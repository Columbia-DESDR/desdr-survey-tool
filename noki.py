from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, request, session, send_from_directory, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import utils
from config import Config
import time
import database
import json
import custom_function_helper
import re
import psycopg2
import followup_job
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, \
    JWTManager
import admin_apis


app = Flask(__name__, static_url_path='', static_folder='frontend/admin-ui/build')
app.config.from_object(Config)
ERROR_MSG = "Sorry, I couldn't understand that. Please try again."
jwt = JWTManager(app)

# # Disable CORS for local testing
# from flask_cors import CORS
# CORS(app)


def trigger_followups(status):
    followup_job.followup(status)


def trigger_active_followups():
    trigger_followups('active')


def trigger_failed_followups():
    trigger_followups('failed')


scheduler = BackgroundScheduler()
scheduler.add_job(trigger_active_followups, CronTrigger.from_crontab('15 6,11,19 * * *'))
scheduler.add_job(trigger_failed_followups, CronTrigger.from_crontab('1 9,13,21 * * *'))
scheduler.start()


@app.route('/token', methods=["POST"])
def auth_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != app.config['ADMIN_USER'] or password != app.config['ADMIN_PWD']:
        return {"msg": "Invalid username or password"}, 401

    token = create_access_token(identity=username)
    response = {"token": token}
    return response


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        target_timestamp = datetime.timestamp(datetime.now(timezone.utc) + timedelta(minutes=30))
        if target_timestamp > get_jwt()["exp"]:
            token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["token"] = token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response


# Session has the following information:
#     deployment_name   : string  : indicates name of the deployment
#     step_name         : string  : indicates the current step
#     awaiting_response : yes/no  : 'yes' indicates that the current step's msg is already sent
#                                   and response from user is awaited
#
# Following params from request is used:
#     Body  : user's response
#     From  : user's number
@app.route("/sms", methods=["GET", "POST"])
def incoming_sms():
    """
        The incoming_sms function is the main function that handles incoming SMS messages.
        It takes in a request from Twilio, and returns a response to Twilio.
        The request contains information about the message sent by the user, including:
            - The phone number of the sender (From)
            - The body of their message (Body)

        :return: A twiml response
        :doc-author: Aby (using Trelent AI)
    """
    try:
        database.close_connection()
        database.reconnect()
        return incoming_sms_handler()

    except psycopg2.Error as e:
        print("SQL error", e)
        database.rollback_on_error()
        return get_error_resp()
    except Exception as e:
        print("Some error occurred", e)
        return get_error_resp()


def incoming_sms_handler():
    """
        The incoming_sms_handler function is the main function that handles incoming SMS messages.
        It first checks if the user has already started a survey, and if not, it starts one by setting
        the deployment_name to be equal to the body of their message. It then fetches this deployment from
        the database using its name as an identifier. If no such deployment exists in our database, we return
        an error response (see get_error_resp()). Otherwise, we trigger user onboarding (see onboard_user()) and
        then check whether or not they want to restart their survey by checking for a match with the 'restart

        :return: A twiml response
        :doc-author: Aby (using Trelent AI)
    """
    deployment_name = session.get("deployment_name", None)
    step_name = session.get("step_name", None)
    awaiting_response = session.get("awaiting_response", None)

    body = request.values.get("Body", None)

    # check if this is a special message to exit a survey!
    if body.lower() == '#bye':
        session["deployment_name"] = None
        session["step_name"] = None
        session["awaiting_response"] = None
        return get_twilio_resp('Bye! Until next time.')

    # check if this is a special message to remove followups!
    if body.lower() == '#optout':
        session["deployment_name"] = None
        session["step_name"] = None
        session["awaiting_response"] = None
        followup_opt_out()
        return get_twilio_resp('Bye! Until next time.')

    # if deployment is None, this should be the start message
    if deployment_name is None or step_name is None:
        user_start_message = body.lower()
        results = database.get_deployment_by_user_start_message(user_start_message)
        if not results:
            return get_error_resp()
        deployment_name = results['deployment_name']
        step_name = 'start'
        awaiting_response = 'no'

    # fetch the deployment from DB using 'deployment_name'
    results = database.get_deployment_by_name(deployment_name)
    if not results:
        return get_error_resp()

    deployment = json.loads(results['script'])
    if deployment is None or deployment == {} or 'survey' not in deployment:
        return get_error_resp()

    deployment['deployment_name'] = results['deployment_name']
    deployment['user_start_message'] = results['user_start_message']
    deployment['instance_name'] = results['instance_name']

    # Trigger user onboarding if User not present in DB
    user_number, user_id = onboard_user(deployment_name)

    # **** the actual survey logic starts here **** #

    # check if the user wants to restart
    if body.lower() == deployment['restart_word']:
        step_name = "start"
        session["step_name"] = "start"
        session["awaiting_response"] = None
        awaiting_response = "no"

    # if awaiting_response is 'yes', save step's response & get next step
    if awaiting_response == 'yes':
        save_response(body, deployment, step_name, user_number, user_id)
        step_name = get_next_step(deployment, step_name, user_number)

    # send msgs of next step
    msgs = get_msgs(step_name, deployment, user_number)
    for i in range(len(msgs) - 1):
        send_twilio_resp(request, msgs[i])
        time.sleep(2)
    current_step = deployment['survey'][step_name]
    if ('next' in current_step and current_step['next'] != '') or \
            ('next_condition' in current_step) or ('next_function' in current_step):
        session["deployment_name"] = deployment_name
        session["step_name"] = step_name
        session["awaiting_response"] = 'yes'
    else:
        # adding this response to the DB to track that the user completed the survey
        database.insert_response(user_number, '$END_SURVEY$', '-', deployment['deployment_name'], msgs[-1],
                                 current_step['type'], user_id)
        followup(deployment, user_number)
        session["deployment_name"] = None
        session["step_name"] = None
        session["awaiting_response"] = None
    return get_twilio_resp(msgs[-1])


def followup(deployment, user_id):
    """
    The followup function is used to schedule followup deployments for a user.
    It takes in the deployment name and the user_id as parameters.
    The function first gets all the followup scripts from that deployment, then iterates through them one by one.
    For each script, it checks if there is already a active followup scheduled for that particular script and if so,
    sets its status to ignore (so it doesn't get executed).
    Then it inserts a new entry into the database with status 'active' and sets its execution date based on what type
    of delay was specified in the config file.

    :param deployment: Get the name of the deployment
    :param user_id: Identify the user in the database
    :return: The name of the next deployment
    :doc-author: Aby (using Trelent)
    """
    if 'followup' not in deployment:
        return
    followup_scripts = deployment['followup']
    followups = set()
    for followup_script in followup_scripts:
        # delay calculation
        delay = followup_script['delay']
        followup_on = ''
        interval = ''
        if delay['type'] == 'interval':
            value = delay['value']
            followup_on = utils.get_next_date_from_delay(value)
            interval = delay['value']
        elif delay['type'] == 'custom_function':
            value = delay['value']
            function_name = value['function_name']
            args = value['args']
            followup_on = custom_function_helper.function_caller(session, function_name, deployment['deployment_name'], None,
                                                                 user_id, args)
        elif delay['type'] == 'exact_date':
            followup_on = delay['value']

        # end date calculation
        end_date = ''
        if delay['type'] == 'interval' and 'end' in followup_script:
            end = followup_script['end']
            if end['type'] == 'interval':
                value = end['value']
                end_date = utils.get_next_date_from_delay(value)
            elif end['type'] == 'custom_function':
                value = end['value']
                function_name = value['function_name']
                args = value['args']
                end_date = custom_function_helper.function_caller(session, function_name, deployment['deployment_name'], None,
                                                                  user_id, args)
            elif end['type'] == 'exact_date':
                end_date = end['value']

        if followup_on != '':
            if 'deployment_name_condition' in followup_script:
                function_name = followup_script['deployment_name_condition']['function_name']
                args = followup_script['deployment_name_condition']['args']
                answer_next_map = followup_script['deployment_name_condition']['answer_next_map']
                to_deployment = next_condition_evaluate(function_name, answer_next_map, deployment['deployment_name'],
                                                        "",
                                                        user_id, args)
            else:
                to_deployment = followup_script['deployment_name']
            if not to_deployment or to_deployment == '':
                continue
            followups.add((followup_on, to_deployment, interval, end_date))
            active_followups = database.get_active_followup(user_id=user_id,
                                                            from_deployment=deployment['deployment_name'],
                                                            to_deployment=to_deployment)
            for active_followup in active_followups:
                database.set_followup_status_ignore(user_id=user_id, status=active_followup['status'],
                                                    from_deployment=deployment['deployment_name'],
                                                    to_deployment=to_deployment)

    for followup_on, to_deployment, interval, end_date in followups:
        database.insert_followup(user_id=user_id, status='active', from_deployment=deployment['deployment_name'],
                                 to_deployment=to_deployment, followup_on=followup_on,
                                 repeat_every=interval, end_date=end_date)


def save_response(body, deployment, step_name, user_number, hashed_user_id):
    """
        The save_response function saves the user's response to a question in the database.

        :param body: Store the response from the user
        :param deployment: Get the survey steps
        :param step_name: Identify the step in the survey
        :param user_number: user number
        :param hashed_user_id: unique id of the user
        :return: Nothing
        :doc-author: Aby (using Trelent AI)
    """
    msgs = get_msgs(step_name, deployment, user_number)
    current_step = deployment['survey'][step_name]
    if current_step['type'] == 'var':
        database.insert_response(user_number, step_name, body, deployment['deployment_name'], msgs[-1],
                                 current_step['type'], hashed_user_id)
    elif current_step['type'] == 'mcq':
        selected_option = re.search(r'\d+', body).group(0)  # regex to get a number from msg
        if selected_option in current_step['options'].keys():
            database.insert_response(user_number, step_name, current_step['options'][selected_option],
                                     deployment['deployment_name'], msgs[-1], current_step['type'], hashed_user_id)
        else:
            raise Exception('The input doesn\'t match the available options!')


def next_condition_evaluate(function_name, answer_next_map, deployment_name, step_name, user_number, args):
    answer = custom_function_helper.function_caller(session, function_name, deployment_name,
                                                    step_name, user_number, args)
    try:
        answer = float(answer)
        answer_float = True
    except ValueError:
        answer_float = False

    def type_cast(is_float, x):
        if is_float:
            return float(x)
        else:
            return x

    for k, v in answer_next_map.items():
        if k[:2] == '<=':
            if type_cast(answer_float, answer) <= type_cast(answer_float, k[2:]):
                return v
        elif k[:2] == '>=':
            if type_cast(answer_float, answer) >= type_cast(answer_float, k[2:]):
                return v
        elif k[:1] == '<':
            if type_cast(answer_float, answer) < type_cast(answer_float, k[1:]):
                return v
        elif k[:1] == '>':
            if type_cast(answer_float, answer) > type_cast(answer_float, k[1:]):
                return v
        elif k[:2] == '==':
            if type_cast(answer_float, answer) == type_cast(answer_float, k[2:]):
                return v
        elif k[:7] == 'between':
            _, v1, v2 = k.split(',')
            if type_cast(answer_float, v1) <= type_cast(answer_float, answer) <= type_cast(answer_float, v2):
                return v
        elif type_cast(answer_float, answer) == type_cast(answer_float, k):
            return v


def get_next_step(deployment, step_name, user_number):
    """
        The get_next_step function takes in a deployment and step name, and returns the next step.
        If there is no 'next' key in the current_step dictionary, then it looks for a 'next_condition' key.
        If there is one, it gets all responses from that user to that question.
        It then finds the latest response to that question (the most recent) and uses its answer as an index into
        next_condition's answer_next map.

        :param deployment: Get the survey and deployment name
        :param step_name: Get the current step from the survey
        :param user_number: Get the user's phone number
        :return: The next step in the survey
        :doc-author: Aby (using Trelent AI)
    """
    current_step = deployment['survey'][step_name]
    if 'next' in current_step:
        return current_step['next']
    elif 'next_condition' in current_step:
        function_name = current_step['next_condition']['function_name']
        args = current_step['next_condition']['args']
        answer_next_map = current_step['next_condition']['answer_next_map']
        return next_condition_evaluate(function_name, answer_next_map, deployment['deployment_name'], step_name,
                                       user_number, args)

    raise Exception('Cannot evaluate the next step from the available options!')


def followup_opt_out():
    user_number = str(utils.extract_number(str(request.values.get("From"))))
    database.followup_opt_out(user_id=user_number)


def onboard_user(deployment_name):
    """
        The onboard_user function is used to onboard a user into the system.
        It takes in the deployment name as an argument and returns the user's phone number.
        If a new user, it will insert them into the database with their phone number, username (deployment name),
        status (active) and role ('default'). If they are already in our database but have not been assigned to this
        deployment yet, we update their username column with this deployment's name.

        :param deployment_name: Identify the deployment that the user is trying to access
        :return: The user's phone number
        :doc-author: Aby (using Trelent AI)
    """
    user_number = str(utils.extract_number(str(request.values.get("From"))))
    from_user = database.get_user_by_id(user_number)
    # storing deployment name in username column
    if not from_user:
        database.insertUser(user_number, deployment_name, 1, 'default')
    elif from_user['username'] != deployment_name:
        database.update_username(user_number, deployment_name)
    user_id = database.get_user_by_id(user_number)['id']
    return user_number, user_id


def get_twilio_resp(msg):
    resp = MessagingResponse()
    resp.message(msg)
    return str(resp)


def get_error_resp(error_msg=ERROR_MSG):
    return get_twilio_resp(error_msg)


def send_twilio_resp(request, msg):
    user_number = request.values.get("From")
    noki_number = request.values.get("To")
    utils.send_message(msg, from_number=noki_number, to_number=user_number)


def get_msgs(step_name, deployment, user_number):
    """
        The get_msgs function takes in the step name, deployment and user number as parameters.
        It then creates an empty dictionary called params. It then gets the current step from the survey
        and checks if there are any parameters for that particular step. If there are, it loops through each parameter
        and calls a custom function helper to get its value using its function name and arguments (if any). The key of this
        parameter is added to params with its value being what was returned by calling the custom function helper.

        :param step_name: Identify the step in the survey
        :param deployment: Get the deployment name
        :param user_number: Identify the user
        :return: A list of messages to be sent to the user
        :doc-author: Aby (using Trelent AI)
    """
    params = {}
    current_step = deployment['survey'][step_name]
    if 'params' in current_step:
        for k, v in current_step['params'].items():
            function_name = v['function_name']
            args = v['args']
            param_value = custom_function_helper.function_caller(session, function_name, deployment['deployment_name'],
                                                                 step_name,
                                                                 user_number, args)
            params[k] = param_value

    msgs = []
    for i in range(len(current_step['msgs'])):
        msg = current_step['msgs'][i]
        param_keys = set(re.findall(r'%%(.*?)%%', msg))
        for k in param_keys:
            msg = msg.replace(f'%%{k}%%', params[k])
        msgs.append(msg)
    if current_step['type'] == 'mcq':
        for k, v in current_step['options'].items():
            msgs[-1] += '\n' + k + '. ' + v
    return msgs


@app.route("/deployment", methods=["GET", "POST", "PUT"])
@jwt_required()
def deployment_crud():
    database.close_connection()
    database.reconnect()
    if request.method == 'POST':
        body = request.json
        return admin_apis.add_deployment(body)
    if request.method == 'GET':
        args = request.args
        if 'deployment_name' in args:
            return admin_apis.get_deployment(args['deployment_name'])
        else:
            return admin_apis.get_all_deployments()
    if request.method == 'PUT':
        body = request.json
        return admin_apis.edit_deployment(body)


@app.route("/deployment-stats", methods=["GET"])
@jwt_required()
def deployment_stats():
    database.close_connection()
    database.reconnect()
    args = request.args
    return admin_apis.get_deployment_stats(args['deployment_name'])


@app.route("/favicon.ico")
def serve_favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')


@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(app.static_folder, 'manifest.json')


@app.route("/", defaults={'path': ''})
@app.route("/<path>")
@app.route("/<path1>/<path2>")
def serve_ui(path=None, path1=None, path2=None):
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(use_reloader=False, debug=True)

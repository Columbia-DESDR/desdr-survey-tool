import database
import utils
from datetime import datetime


followup_msg_template = "Hey, it's Noki. If you want an update on {{1}}, please reply with the phrase *{{2}}*"
noki_number = '16462170881'


def followup(status='active'):
    result = database.get_valid_followups(status)
    user_followup_map = {}
    for row in result:
        user_number = 'N/A'
        to_deployment = 'N/A'
        try:
            user_number = row['user_id']
            to_deployment = row['to_deployment']
            deployment = database.get_deployment_by_name(to_deployment)
            if not deployment:
                raise Exception('Deployment not found!')
            user_start_message = deployment['user_start_message']
            msg = followup_msg_template.replace('{{1}}', 'Climate').replace('{{2}}', user_start_message)
            user_followup_map[user_number] = {'msg': msg, 'followup_row': row}
        except Exception as e:
            print(f'Followup error. number: {user_number}, deployment: {to_deployment}. Error: {e}')

    for user_number, msg_object in user_followup_map.items():
        row = msg_object['followup_row']
        try:
            utils.send_message(msg_object['msg'], to_number="whatsapp:+" + user_number, from_number="whatsapp:+" + noki_number)
            if row['repeat_every'] is None or row['repeat_every'] == '':
                database.update_followup(status='success', id=row['id'], followup_on=row['followup_on'],
                                         last_successful_followup=datetime.today().strftime('%Y-%m-%d'))
            else:
                followup_on = utils.get_next_date_from_delay(row['repeat_every'])
                database.update_followup(status='active', id=row['id'], followup_on=followup_on,
                                         last_successful_followup=datetime.today().strftime('%Y-%m-%d'))
        except Exception as e:
            print(f'Error sending followup msg to {user_number}, msg: {msg_object["msg"]}. Error: {e}')
            database.update_followup(status='failed', id=row['id'], followup_on=row['followup_on'],
                                     last_successful_followup=row['last_successful_followup'])

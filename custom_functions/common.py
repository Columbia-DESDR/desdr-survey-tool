import datetime


def get_from_response(default, args):
    """
        The get_from_response function takes in a list of arguments and returns the latest response from that user
        for that step. The function is used to get responses from previous steps in order to use them as inputs for
        later steps.

        :param default: Pass the deployment_name, step_name and user_number to the get_from_response function
        :param args
        :return: The answer to the question
        :doc-author: Aby (using Trelent AI)
    """
    deployment_name, _, user_number = default[:3]
    step_name_to_fetch = args[0]
    database = default[-1]
    return get_latest_response(database, deployment_name, step_name_to_fetch, user_number)


def get_latest_response(database, deployment_name, step_name_to_fetch, user_number):
    result = database.get_response_by_user_step_deployment(user_number, step_name_to_fetch, deployment_name)
    latest = result[0]['created_at']
    latest_row = result[0]
    for row in result:
        if row['created_at'] > latest:
            latest = row['created_at']
            latest_row = row
    return latest_row['answer']


def get_current_date(default, args):
    return datetime.datetime.today().strftime(args[0])


functions = {
    'get_from_response': get_from_response,
    'get_current_date': get_current_date
}

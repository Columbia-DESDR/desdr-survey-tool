import database


def get_all_deployments():
    return database.get_all_deployments()


def get_deployment(deployment_name):
    return database.get_deployment_by_name(deployment_name)


def get_deployment_stats(deployment_name):
    res = database.get_deployment_stats(deployment_name)
    unique_res = database.get_unique_deployment_stats(deployment_name)
    return {'step_wise_stats': res, 'step_wise_unique_stats': unique_res}


def add_deployment(data):
    deployment_name = data["deployment_name"]
    user_start_message = data["user_start_message"]
    instance_name = data["instance_name"]
    comments = data["comments"]
    script = data["script"]
    result_name = database.get_deployment_by_name(deployment_name)
    result_start_msg = database.get_deployment_by_user_start_message(user_start_message)
    if result_name or result_start_msg:
        return {"error": "deployment name or start message already exists!"}
    else:
        database.insert_deployment(deployment_name, instance_name, script, user_start_message, comments)
        return {"msg": "success"}


def edit_deployment(data):
    deployment_name = data["deployment_name"]
    user_start_message = data["user_start_message"]
    instance_name = data["instance_name"]
    comments = data["comments"]
    script = data["script"]
    result_name = database.get_deployment_by_name(deployment_name)
    if not result_name:
        return {"error": "deployment does not exist"}
    else:
        database.insert_deployment_snapshot(deployment_name, instance_name, script, user_start_message, comments)
        database.update_deployment(deployment_name, instance_name, script, user_start_message, comments)
        return {"msg": "success"}

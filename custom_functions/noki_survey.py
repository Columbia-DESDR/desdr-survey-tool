from . import common
import datetime


def noki_delay_calc(default, args):
    deployment_name, _, user_number = default[:3]
    month_step, time_step = args[0], args[1]
    month = common.get_from_response(default, [month_step])
    time = common.get_from_response(default, [time_step])
    month_num = datetime.datetime.strptime(month, '%B').strftime('%m')
    day = '05'
    if time == 'Early':
        day = '05'
    elif time == 'Mid':
        day = '15'
    elif time == 'Late':
        day = '25'
    current_year = datetime.datetime.now().strftime("%Y")
    parsed_date = current_year + '-' + month_num + '-' + day
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    if current_date > parsed_date:
        year = str(int(current_year) + 1)
        parsed_date = year + '-' + month_num + '-' + day
    return parsed_date


def noki_next_step_after_planting_start_detail(default, args):
    database = default[-1]
    random_id = database.getRandomId(default[2])
    if random_id == 0:
        return 'start_model_prediction_0'
    else:
        return 'start_model_prediction_1'


def noki_next_step_after_planting_end_detail(default, args):
    database = default[-1]
    random_id = database.getRandomId(default[2])
    if random_id == 0:
        return 'end_model_prediction_0'
    else:
        return 'end_model_prediction_1'


def noki_prediction(args):
    return 'above normal'


def noki_model_name(args):
    return 'Next Gen'


def noki_past_data(args):
    return 'below normal'


functions = {
    'noki_delay_calc': noki_delay_calc,
    'noki_next_step_after_planting_start_detail': noki_next_step_after_planting_start_detail,
    'noki_next_step_after_planting_end_detail': noki_next_step_after_planting_end_detail,
    'noki_model_name': noki_model_name,
    'noki_prediction': noki_prediction,
    'noki_past_data': noki_past_data
}

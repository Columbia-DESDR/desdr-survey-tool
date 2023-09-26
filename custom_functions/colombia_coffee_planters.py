import calendar
import datetime

from . import common

month_index_map = {month: index - 1 for index, month in enumerate(calendar.month_name) if month}
index_month_map = {index - 1: month for index, month in enumerate(calendar.month_name) if month}


def ccp_get_past_three_months(default, args):
    # the args here would be the same as for get_from_response
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    database = default[-1]
    year = int(datetime.datetime.today().strftime('%Y'))
    print(month_val, year)
    row = database.get_forecast(month_val, year)
    while not row:
        row = database.get_forecast(month_val, year - 1)
        if row:
            break
        month_val = month_val - 1 if month_val > 1 else 12
    m1 = (month_val - 3) % 12
    m2 = (month_val - 2) % 12
    m3 = (month_val - 1) % 12
    return f'{index_month_map[m1]}-{index_month_map[m2]}-{index_month_map[m3]}'


def ccp_fetch_last_5_years_rainfall(default, args):
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    database = default[-1]
    year = int(datetime.datetime.today().strftime('%Y'))
    row = database.get_forecast(month_val, year)
    while not row:
        row = database.get_forecast(month_val, year - 1)
        month_val -= 1
    return str(int(float(row['obs_recent'])))


def ccp_get_poe(default, args):
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    database = default[-1]
    year = int(datetime.datetime.today().strftime('%Y'))
    row = database.get_forecast(month_val, year)
    percent = float(row['poe']) * 100
    return str(int(percent))


def ccp_get_poe_qualitative(default, args):
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    database = default[-1]
    year = int(datetime.datetime.today().strftime('%Y'))
    row = database.get_forecast(month_val, year)
    percent = float(row['poe']) * 100
    if percent > 60:
        return 'HIGH'
    elif percent > 49:
        return 'MEDIUM'
    else:
        return 'LOW'


def ccp_next_state_after_flowering(default, args):
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    database = default[-1]
    year = int(datetime.datetime.today().strftime('%Y'))
    row = database.get_forecast(month_val, year)
    if not row:
        return 'history_only'
    else:
        user_id = database.get_user_by_id(default[2])['id']
        if user_id % 3 == 0:
            return 'history_forecast_1'
        if user_id % 3 == 1:
            return 'history_forecast_2'
        if user_id % 3 == 2:
            return 'history_forecast_3'


def ccp_get_point_value(default, args):
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    database = default[-1]
    year = int(datetime.datetime.today().strftime('%Y'))
    row = database.get_forecast(month_val, year)
    return str(int(float(row['point_value'])))


def ccp_followup_name(default, args):
    month_name = common.get_from_response(default, [args[1]])
    month_val = month_index_map[month_name]
    current_month = int(datetime.datetime.today().strftime('%m')) - 1
    followup_type = args[0]
    if followup_type == 'pre_season':
        if (month_val - current_month) % 12 <= 1:
            return 'invalid'
        else:
            return 'valid'
    elif followup_type == 'flowering_season':
        if (month_val - current_month) % 12 > 9:
            return 'invalid'
        else:
            return 'valid'
    elif followup_type == 'harvest_season':
        if (month_val - current_month) % 12 > 9:
            return 'invalid'
        else:
            return 'valid'


def ccp_followup_delay(default, args):
    month_name = common.get_from_response(default, [args[1]])
    month_val = month_index_map[month_name]
    current_month = int(datetime.datetime.today().strftime('%m')) - 1
    year = int(datetime.datetime.today().strftime('%Y'))
    followup_type = args[0]
    if followup_type == 'flowering_season':
        month = (month_val + 1) % 12 + 1
        month = month if month >= 10 else "0" + str(month)
        if month_val - current_month > 0:
            return f'{year}-{month}-15'
        else:
            return f'{year + 1}-{month}-15'
    elif followup_type == 'harvest_season':
        month = (month_val + 2) % 12 + 1
        month = month if month >= 10 else "0" + str(month)
        if month_val - current_month > 0:
            return f'{year}-{month}-15'
        else:
            return f'{year + 1}-{month}-15'


def ccp_followup_end(default, args):
    month_name = common.get_from_response(default, args)
    month_val = month_index_map[month_name] + 1
    current_month = int(datetime.datetime.today().strftime('%m'))
    year = int(datetime.datetime.today().strftime('%Y'))
    if month_val - current_month > 0:
        month = month_val if month_val >= 10 else "0" + str(month_val)
        return f'{year}-{month}-01'
    else:
        month = month_val if month_val >= 10 else "0" + str(month_val)
        return f'{year + 1}-{month}-01'


def ccp_prediction_text(default, args):
    database = default[-1]
    month_name = common.get_latest_response(database, 'Colombia coffee planters', 'flowering_season_start', default[2])
    month_val = month_index_map[month_name] + 1
    m1 = (month_val - 3) % 12
    m2 = (month_val - 2) % 12
    m3 = (month_val - 1) % 12
    period = f'{index_month_map[m1]}-{index_month_map[m2]}-{index_month_map[m3]}'

    year = int(datetime.datetime.today().strftime('%Y'))
    current_month = int(datetime.datetime.today().strftime('%m'))
    if current_month < month_val:
        year -= 1
    row = database.get_forecast(month_val, year)
    user_id = database.get_user_by_id(default[2])['id']

    if not row:
        return ''

    point_value = float(row['point_value'])
    poe = float(row['poe']) * 100
    season_total = float(row['season_total'])
    if user_id % 3 == 0:

        msg = f'The Noki’s forecast model predicted that there was a {poe}% chance that the total rainfall ' \
              f'would be the same or more than the average rain during {period} in the  last 5 years.'
        if season_total is None or season_total == '':
            return msg

        msg += ' In fact, it WAS wetter!' if season_total >= point_value else ' In fact, it WAS NOT as wet!'
        user_resp_to_prediction = common.get_latest_response(database, 'Colombia coffee planters', 'history_forecast_1',
                                                             default[2])
    elif user_id % 3 == 1:
        if poe > 60:
            qualitative = 'HIGH'
        elif poe > 49:
            qualitative = 'MEDIUM'
        else:
            qualitative = 'LOW'
        msg = f'The Noki’s forecast model predicted that there was a {qualitative} chance that the total ' \
              f'rainfall would be the same or more than the average rain during {period} in the  last 5 years.'

        if season_total is None or season_total == '':
            return msg

        msg += ' In fact, it WAS wetter!' if season_total >= point_value else ' In fact, it WAS NOT as wet!'
        user_resp_to_prediction = common.get_latest_response(database, 'Colombia coffee planters', 'history_forecast_2',
                                                             default[2])
    else:
        point_value = float(row['point_value'])
        season_total = float(row['season_total'])
        msg = f'The Noki’s forecast model predicted that there would be {point_value} millimeters of rainfall over ' \
              f'the {period} season.'

        if season_total is None or season_total == '':
            return msg

        msg += f' In fact, it WAS {season_total} millimeters!'
        user_resp_to_prediction = common.get_latest_response(database, 'Colombia coffee planters', 'history_forecast_3',
                                                             default[2])

    noki_right = True if point_value >= season_total else False
    if noki_right:
        if user_resp_to_prediction == 'I agree with the forecast':
            msg += ' *You and Noki were right!*'
        elif user_resp_to_prediction == "I don’t know":
            msg += ' *Noki was right*'
        else:
            msg += ' *You were close but Noki was closer*'
    else:
        if user_resp_to_prediction == 'I agree with the forecast' or \
                user_resp_to_prediction == 'I disagree, it is less likely to be as wet':
            msg += ' *You and Noki were close!*'
        elif user_resp_to_prediction == "I don’t know":
            msg += ' *Noki was close*'
        else:
            msg += ' *You were right and Noki was wrong*'
    return msg


functions = {
    'ccp_get_past_three_months': ccp_get_past_three_months,
    'ccp_fetch_last_5_years_rainfall': ccp_fetch_last_5_years_rainfall,
    'ccp_next_state_after_flowering': ccp_next_state_after_flowering,
    'ccp_prediction_text': ccp_prediction_text,
    'ccp_get_poe': ccp_get_poe,
    'ccp_get_poe_qualitative': ccp_get_poe_qualitative,
    'ccp_get_point_value': ccp_get_point_value,
    'ccp_followup_name': ccp_followup_name,
    'ccp_followup_delay': ccp_followup_delay,
    'ccp_followup_end': ccp_followup_end
}

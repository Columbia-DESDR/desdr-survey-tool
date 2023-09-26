import database
from custom_functions import common, colombia_coffee_planters, noki_survey, ikon


function_map = {
    **common.functions,
    **colombia_coffee_planters.functions,
    **noki_survey.functions,
    **ikon.functions
}


def function_caller(session, function_name, deployment_name, step_name, user_number, args):
    return function_map[function_name](default=[deployment_name, step_name, user_number, session, database], args=args)

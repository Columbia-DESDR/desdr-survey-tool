def get_ikon_comparison_string(default, args):
    database = default[-1]
    return '*New York City* vs *Boston*'


def get_ikon_next_step(default, args):
    database = default[-1]
    return 'comparison_question'


functions = {
    'get_ikon_comparison_string': get_ikon_comparison_string,
    'get_ikon_next_step': get_ikon_next_step
}

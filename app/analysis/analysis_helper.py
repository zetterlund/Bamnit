import json


grade_list = [
    'PRE-K',
    'KINDER',
    'FIRST GRADE',
    'SECOND GRADE',
    'THIRD GRADE',
    'FOURTH GRADE',
    'FIFTH GRADE',
    '6',
    '7/8',
    'ELEM',
    'MS',
    'HS'
]


def get_weekday_count():
    with open('app/analysis/stats_dict.txt', 'r') as the_file:
        stats_dict = json.load(the_file)
    return stats_dict['weekday_count']


def get_time_available():
    with open('app/analysis/stats_dict.txt', 'r') as the_file:
        stats_dict = json.load(the_file)
    time_available = stats_dict['time_available']
    time_list = []
    for g in grade_list:
        time_list.append(time_available[g])
    return time_list
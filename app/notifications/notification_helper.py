import json
import ast


topic_list = [
    'grade',
    'subject',
    'language',
    'campus',
]


def get_field_dict():
    with open('app/notifications/field_dict.txt', 'r') as the_file:
        field_dict = json.load(the_file)
    return field_dict


def get_strings(notifications):
    n_strings = {}
    for n in notifications:
        n_strings[n] = {}
        for t in topic_list:
            topic_items = getattr(n, t)
            if topic_items == None:
                topic_items = []
            else:
                topic_items = ast.literal_eval(topic_items)
            n_strings[n][t] = topic_items
    return n_strings
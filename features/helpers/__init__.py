__author__ = 'akoikelov'


def dict_has_keys(keys, dict):
    for k in keys:
        if k not in dict:
            return False

    return True
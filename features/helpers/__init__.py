__author__ = 'akoikelov'


def dict_has_keys(keys, dict):
    for k in keys:
        if k not in dict:
            return False

    return True


def assert_status_code_and_content_type(context, response, status_code, content_type):
    context.test.assertEqual(response['Content-Type'], content_type)
    context.test.assertEqual(response.status_code, status_code)
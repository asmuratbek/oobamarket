__author__ = 'akoikelov'

from allauth.utils import get_user_model
from allauth.account.models import EmailAddress


def dict_has_keys(keys, dict):
    for k in keys:
        if k not in dict:
            return False

    return True


def assert_status_code_and_content_type(context, response, status_code, content_type):
    context.test.assertEqual(response['Content-Type'], content_type)
    context.test.assertEqual(response.status_code, status_code)


def create_user(username, email, password):
    user = get_user_model().objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    email_address = EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)

    return dict(user=user, email_address=email_address)
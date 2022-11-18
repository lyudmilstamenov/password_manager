import getpass
import time
from google.cloud import datastore

from common.consts import LOGIN_OR_SIGNUP_MESSAGE, USER_NOT_FOUND_MESSAGE, WAIT_MESSAGE, HELP_MESSAGE, \
    USER_EXISTS_MESSAGE
from database.datastore_manager import check_user_exists
from database.base import save_entity
from validation import validate_email, validate_password, validate_entity_name

from cryptography import get_hashed_password, check_password

from common.consts import SUCCESSFUL_LOGIN_MESSAGE, SUCCESSFUL_SIGNUP_MESSAGE, LOGGED_IN_MESSAGE, WRONG_PWD_MESSAGE


def signup(app):
    user_info = {'username': validate_entity_name(input('username: '), 'User', 'username',
                                                  lambda value: check_user_exists(app.client, value)),
                 'email': validate_email(input('email: ')), 'password': validate_password(getpass.getpass())}
    user_info['password'] = get_hashed_password(user_info['password'])
    if check_user_exists(app.client, user_info['username']):
        raise ValueError(USER_EXISTS_MESSAGE.format(user_info["username"]))
    user = datastore.Entity(app.client.key('User'))
    save_entity(app.client, user, user_info)
    return SUCCESSFUL_SIGNUP_MESSAGE


def login(app):
    username = input('username: ')
    users = check_user_exists(app.client, username)
    if not users:
        raise ValueError(USER_NOT_FOUND_MESSAGE.format(username))
    user = users[0]
    for i in range(3):
        password = getpass.getpass()
        if check_password(password, user['password']):
            app.user = user
            app.user['password'] = password

            return SUCCESSFUL_LOGIN_MESSAGE.format(username) + LOGGED_IN_MESSAGE.format(username)
        print(WRONG_PWD_MESSAGE.format(2 - i))
    print(WAIT_MESSAGE)
    time.sleep(30)
    return HELP_MESSAGE + LOGIN_OR_SIGNUP_MESSAGE


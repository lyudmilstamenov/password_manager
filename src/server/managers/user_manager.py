"""
Provides method getpass which takes string from the input and hides the characters o the console.
"""
import getpass
import time

from common.consts import LOGIN_OR_SIGNUP_MESSAGE, \
    USER_NOT_FOUND_MESSAGE, WAIT_MESSAGE, HELP_MESSAGE, \
    USER_EXISTS_MESSAGE, SUCCESSFUL_LOGIN_MESSAGE, SUCCESSFUL_SIGNUP_MESSAGE, \
    WRONG_PWD_MESSAGE
from database.datastore_manager import check_user_exists
from database.base import save_entity, create_entity
from security.validation import validate_email, validate_password, validate_entity_name
from security.cryptography import get_hashed_password, check_password


def signup(app):
    """
    Creates a new User entity with name, password and email.
    The name must be unique or it will raise ValueError.
    :param app: App(contains the information about the current state of the programme)
    :return: message for successful sign up
    """
    username = validate_entity_name(app, input('username: '), entity_kind='User')
    user_info = {'name': username,
                 'email': validate_email(input('email: ')),
                 'password': validate_password(getpass.getpass()),
                 'orgs': []}
    user_info['password'] = get_hashed_password(user_info['password'])
    if check_user_exists(app.client, user_info['name']):
        raise ValueError(USER_EXISTS_MESSAGE.format(user_info["name"]))
    user = create_entity(app, 'User')
    save_entity(app.client, user, user_info)
    return SUCCESSFUL_SIGNUP_MESSAGE


def login(app):
    """
    Validates the password of a user with name equal to username and
    sets app.user to this user.
    :param app: App(contains the information about the current state of the programme)
    :return: message for successful log in
    """
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

            return SUCCESSFUL_LOGIN_MESSAGE.format(username, username)
        print(WRONG_PWD_MESSAGE.format(2 - i))
    print(WAIT_MESSAGE)
    time.sleep(30)
    return HELP_MESSAGE + LOGIN_OR_SIGNUP_MESSAGE

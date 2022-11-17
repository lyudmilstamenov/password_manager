import getpass
import time
from google.cloud import datastore

from common.consts import LOGIN_OR_SIGNUP_MESSAGE
from database.datastore_manager import check_user_exists
from database.base import save_entity
from validation import validate_property, validate_email, validate_password, validate_entity_name

from cryptography import get_hashed_password, check_password


def signup(app):
    user_info = {'username': validate_entity_name(input('username: '), 'User', 'username',
                                                  lambda value: check_user_exists(app.client, value)),
                 'email': validate_email(input('email: ')), 'password': validate_password(getpass.getpass())}
    user_info['password'] = get_hashed_password(user_info['password'])
    if check_user_exists(app.client, user_info['username']):
        raise ValueError(f'User with username {user_info["username"]} already exists.')
    user = datastore.Entity(app.client.key('User'))
    save_entity(app.client, user, user_info)
    return LOGIN_OR_SIGNUP_MESSAGE


def login(app):
    username = input('username: ')
    users = check_user_exists(app.client, username)
    if not users:
        raise ValueError(f'User with username {username} does not exist.')
    user = users[0]
    for i in range(3):
        password = getpass.getpass()
        if check_password(password, user['password']):
            app.user = user
            app.user['password'] = password
            print('You have successfully logged in.')
            print(f'Hi {username}, I am your password manager.')
            return ''
        print(f'Wrong password. You have {2 - i} more tries.')
    print('You have to wait 30 sec before continuing.')
    time.sleep(30)
    return LOGIN_OR_SIGNUP_MESSAGE

# def enter_username():
#     username = input('username: ')
#     if is_username_invalid(user_info):
#         print('Invalid username. Enter valid username or enter "exit" to exit the sign up process')
#         username= enter_username()

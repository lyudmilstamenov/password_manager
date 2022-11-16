import getpass
import os
import time
from google.cloud import datastore

from consts import LOGIN_OR_SIGNUP_MESSAGE
from utils import check_user_exists


def signup(app):
    user_info = {}
    user_info['username'] = input('username: ')
    user_info['email'] = input('email: ')
    user_info['password'] = getpass.getpass()
    if check_user_exists(app.client,user_info['username']):
        raise ValueError(f'User with username {user_info["username"]} already exists.')
    user = datastore.Entity(app.client.key('User'))
    user.update(user_info)
    app.client.put(user)
    return LOGIN_OR_SIGNUP_MESSAGE

def login(app):
    username = input('username: ')
    users = check_user_exists(app.client,username)
    if not users:
        raise ValueError(f'User with username {username} does not exist.')
    user = users[0]
    for i in range(3):
        password = getpass.getpass()
        if password == user['password']:
            app.user = user
            print('You have successfully logged in.')
            print(f'Hi {username}, I am your password manager.')
            return ''
        print(f'Wrong password. You have {2-i} more tries.')
    print('You have to wait 30 sec before continuing.')
    time.sleep(30)
    return LOGIN_OR_SIGNUP_MESSAGE


# def enter_username():
#     username = input('username: ')
#     if is_username_invalid(user_info):
#         print('Invalid username. Enter valid username or enter "exit" to exit the sign up process')
#         username= enter_username()


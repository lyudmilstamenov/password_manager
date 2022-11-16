import getpass
import os
from google.cloud import datastore
from utils import check_user_exists
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='E:/Hobbies/coding/personal_projects/password_function/credentials.json'

client = datastore.Client()

def signup():
    user_info = {}
    user_info['username'] = input('username: ')
    user_info['email'] = input('email: ')
    user_info['password'] = getpass.getpass()
    if check_user_exists(client,user_info['username']):
        raise ValueError(f'User with username {user_info["username"]} already exists.')
    user = datastore.Entity(client.key('User'))
    user.update(user_info)
    client.put(user)

def login():
    username = input('username: ')
    users = check_user_exists(client,username)
    if not users:
        raise ValueError(f'User with username {username} does not exist.')
    user = users[0]
    for _ in range(3):
        password = getpass.getpass()
        if password == user['password']:
            user = user


# def enter_username():
#     username = input('username: ')
#     if is_username_invalid(user_info):
#         print('Invalid username. Enter valid username or enter "exit" to exit the sign up process')
#         username= enter_username()


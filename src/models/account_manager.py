from getpass import getpass

import pyperclip
from google.cloud import datastore

from common.account_consts import URL_OPENED_MESSAGE, URL_NOT_VALID_MESSAGE
from models.category_manager import add_account_to_category, update_category
from common.utils import visualize_accounts
from database.datastore_manager import check_account_exists
from database.base import save_entity
from validation import validate_string_property, validate_email, validate_url, validate_password

from validation import validate_entity_name

from common.account_consts import ACCOUNT_EXISTS_MESSAGE, SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, \
    COPIED_TO_CLIPBOARD_MESSAGE, SHOW_PWD_MESSAGE, DELETED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, \
    UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE, ACCOUNT_NAME_INPUT_MESSAGE, APP_NAME_INPUT_MESSAGE, LOGIN_URL_INPUT_MESSAGE, \
    CATEGORY_INPUT_MESSAGE, USERNAME_INPUT_MESSAGE, EMAIL_INPUT_MESSAGE, NOTES_INPUT_MESSAGE, PWD_INPUT_MESSAGE, \
    ACCOUNT_NOT_FOUND_MESSAGE
from cryptography import encrypt, decrypt
from validators import url as url_validator
from database.datastore_manager import retrieve_all_accounts_by_user


def add_account(app):
    account_info = populate_account_info(app)
    account_info['password'] = encrypt(account_info['password'], app.user['password'])
    account_info['owner'] = app.user.key
    if check_account_exists(app.client, account_info['account_name'], app.user):
        raise ValueError(ACCOUNT_EXISTS_MESSAGE.format(account_info["account_name"]))
    account = datastore.Entity(app.client.key('Account'))
    save_entity(app.client, account, account_info)
    add_account_to_category(app, account_info['category'], account.key)
    app.last_account = account
    return SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE.format(account_info['account_name'], app.user['username'])


def edit_account(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    account_info = dict(account)
    print(UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE)
    new_account_info = populate_account_info(app, True)
    if new_account_info['category']:
        update_category(app, account_info['category'], new_account_info['category'], account.key)
    if new_account_info['password']:
        new_account_info['password'] = encrypt(new_account_info['password'], app.user['password'])
    for key, value in new_account_info.items():
        if value:
            account_info[key] = value
            continue
        if value == '-del':
            account[key] = ''

    save_entity(app.client, account, account_info)
    app.last_account = account
    return UPDATED_ACCOUNT_MESSAGE.format(account_info['account_name'], app.user['username'])


def delete_account(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    app.client.delete(account.key)
    app.last_account = None
    return DELETED_ACCOUNT_MESSAGE.format(account['account_name'], app.user['username'])


def view_account(app, command):
    if command == '-all':
        return view_all_accounts(app)
    return view_account_by_account_name(app, command)


def view_all_accounts(app):
    accounts = retrieve_all_accounts_by_user(app.client, app.user)
    visualize_accounts(app.user['username'], accounts)
    app.last_account = None
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['username'])


def view_account_by_account_name(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    visualize_accounts(app.user['username'], [account])
    app.last_account = account
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['username'])


def visualize_password(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    password = decrypt(account['password'], app.user['password'])  # decrypt
    app.last_account = account
    return SHOW_PWD_MESSAGE.format(password, app.user['username'])


def copy_password(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    password = decrypt(account['password'], app.user['password'])  # decrypt
    pyperclip.copy(password)
    app.last_account = account
    return COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['username'])


def open_url(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    url = account['login_url']
    if url and url_validator(url):
        import webbrowser
        webbrowser.open(url)
        return URL_OPENED_MESSAGE.format(app.user['username'])
    return URL_NOT_VALID_MESSAGE.format(app.user['username'])


def retrieve_account_by_account_name(app, account_name):
    if app.last_account and account_name == app.last_account['account_name']:
        return app.last_account
    if not (accounts := check_account_exists(app.client, account_name, app.user)):
        raise ValueError(ACCOUNT_NOT_FOUND_MESSAGE.format(account_name))
    return accounts[0]


def populate_account_info(app, can_be_empty=False):
    account_info = {
        'account_name': validate_entity_name(input(ACCOUNT_NAME_INPUT_MESSAGE),
                                             'Account',
                                             'account name',
                                             lambda value: check_account_exists(app.client, value, app.user),
                                             can_be_empty),
        'app_name': validate_string_property(input(APP_NAME_INPUT_MESSAGE), 'app name', True),
        'login_url': validate_url(input(LOGIN_URL_INPUT_MESSAGE)),
        'category': validate_string_property(input(CATEGORY_INPUT_MESSAGE), 'category', True),
        'username': validate_string_property(input(USERNAME_INPUT_MESSAGE), 'username', can_be_empty),
        'email': validate_email(input(EMAIL_INPUT_MESSAGE), can_be_empty),
        'notes': input(NOTES_INPUT_MESSAGE),
        'password': validate_password(getpass(PWD_INPUT_MESSAGE), skip_validation=True, can_be_empty=can_be_empty)
    }
    account_info['pwd_length'] = len(account_info['password'])
    return account_info

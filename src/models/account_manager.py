from getpass import getpass

import pyperclip
from google.cloud import datastore

from models.category_manager import add_account_to_category, remove_account_from_category
from common.utils import visualize_accounts
from database.datastore_manager import check_account_exists
from database.base import save_entity
from validation import validate_string_property, validate_email, validate_url, validate_password

from validation import validate_entity_name

from common.consts import ACCOUNT_EXISTS_MESSAGE


def add_account(app):
    account_info = populate_account_info(app)
    account_info['owner'] = app.user.key
    if check_account_exists(app.client, account_info['account_name'], app.user):
        raise ValueError(ACCOUNT_EXISTS_MESSAGE.format(account_info["account_name"]))
    account = datastore.Entity(app.client.key('Account'))
    save_entity(app.client, account, account_info)
    add_account_to_category(app, account_info['category'], account.key)
    print(f'Account with {account_info["account_name"]} was successfully created.')
    app.last_account = account


def update_category(app, old_category_name, new_category_name, account_key):
    if new_category_name == old_category_name:
        return
    if old_category_name:
        remove_account_from_category(app, old_category_name, account_key)

    if new_category_name == '-del':
        add_account_to_category(app, '', account_key)
    else:
        add_account_to_category(app, new_category_name, account_key)


def edit_account(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    account_info = dict(account)
    print('In order not to change the following property click "enter"')
    new_account_info = populate_account_info(app, True)
    if new_account_info['category']:
        update_category(app, account_info['category'], new_account_info['category'], account.key)
    for key, value in new_account_info.items():
        if value:
            account_info[key] = value
            continue
        if value == '-del':
            account[key] = ''

    save_entity(app.client, account, account_info)
    print(f'Account with {account_info["account_name"]} was successfully updated.')
    app.last_account = account
    return


def delete_account(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    app.client.delete(account.key)
    app.last_account = None
    print(f'Account with account name {account["account_name"]} was successfully deleted.')


def view_account(app, command):
    if command == '-all':
        return view_all_accounts(app)
    return view_account_by_account_name(app, command)


def view_all_accounts(app):
    query = app.client.query(kind='Account')
    visualize_accounts(app.user['username'], list(query.fetch()))
    app.last_account = None
    return 'msg'


def view_account_by_account_name(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    visualize_accounts(app.user['username'], [account])
    app.last_account = account
    return 'msg'


def populate_account_info(app, can_be_empty=False):
    account_info = {
        'account_name': validate_entity_name(input('account name (This name must be unique per account.): '), 'Account',
                                             'account name',
                                             lambda value: check_account_exists(app.client, value, app.user),
                                             can_be_empty),
        'app_name': validate_string_property(input('app name []: '), 'app name', True),
        'login_url': validate_url(input('login url []: ')),
        'category': validate_string_property(input('category []: '), 'category', True),
        'username': validate_string_property(input('username: '), 'username', can_be_empty),
        'email': validate_email(input('email: '), can_be_empty),
        'notes': input('notes: '),
        'password': validate_password(getpass('password: '))}
    # TODO add encryption of pwd
    account_info['pwd_length'] = len(account_info['password'])
    return account_info


def visualize_password(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    password = account['password']  # decrypt
    print(f'Your password is {password}.')
    app.last_account = account


def copy_password(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    password = account['password']  # decrypt
    pyperclip.copy(password)
    print('The password was successfully copied to your clipboard.')
    app.last_account = account


def retrieve_account_by_account_name(app, account_name):
    if app.last_account and account_name == app.last_account['account_name']:
        return app.last_account
    if not (accounts := check_account_exists(app.client, account_name, app.user)):
        raise ValueError(f'Account with account name {account_name} was not found.')
    return accounts[0]

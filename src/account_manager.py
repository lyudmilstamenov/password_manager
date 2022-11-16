from getpass import getpass

import tabulate
import pyperclip
from google.cloud import datastore

from category_manager import add_account_to_category,remove_account_from_category
from utils import check_account_exists
from consts import ACCOUNT_PROPERTIES, ACCOUNTS_ORDER


def add_account(app):
    account_info = populate_account_info()
    account_info['owner'] = app.user.key
    if check_account_exists(app.client, account_info['account_name'],app.user):
        raise ValueError(f'Account with account name {account_info["account_name"]} already exists.')
    account = datastore.Entity(app.client.key('Account'))
    account.update(account_info)
    app.client.put(account)
    add_account_to_category(app,account_info['category'],account.key)
    print(f'Account with {account_info["account_name"]} was successfully created.')
    app.last_account = account


def update_category(app,old_category_name, new_category_name,account_key):
    if new_category_name  != old_category_name and old_category_name:
        remove_account_from_category(app.cl,old_category_name,account_key)
    if new_category_name != old_category_name and new_category_name:
        add_account_to_category(app,new_category_name,account_key)


def edit_account(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    account_info = dict(account)
    print('In order not to change the following property click "enter"')
    new_account_info = populate_account_info()

    for key, value in new_account_info.items():
        if value:
            account_info[key] = value

    account.update(account_info)
    app.client.put(account)
    update_category(app,account_info['category'],new_account_info['category'],account.key)
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
    view_account_by_account_name(app, command)


def view_all_accounts(app):
    query = app.client.query(kind='Account')
    visualize_accounts(list(query.fetch()))


def view_account_by_account_name(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    visualize_accounts([account])
    app.last_account = account


def populate_account_info():
    account_info = {}
    account_info['account_name'] = input('account name (This name must be unique per account.): ')
    account_info['app_name'] = input('app name []: ')
    account_info['login_url'] = input('login url []: ')
    account_info['category'] = input('category []: ')
    account_info['username'] = input('username: ')
    account_info['email'] = input('email: ')
    account_info['notes'] = input('notes: ')
    account_info['password'] = getpass('password: ')
    # TODO add encryption of pwd
    account_info['pwd_length'] = len(account_info['password'])
    return account_info


def drop_sensitive_info(account):
    account['password'] = '*' * account['pwd_length']
    del account['pwd_length']
    return account


def visualize_password(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    password = account['password']  # decrypt
    print(f'Your password is {password}.')


def copy_password(app, account_name):
    account = retrieve_account_by_account_name(app, account_name)
    password = account['password']  # decrypt
    pyperclip.copy(password)
    print('The password was successfully copied to your clipboard.')


def retrieve_account_by_account_name(app, account_name):
    if app.last_account and account_name == app.last_account['account_name']:
        return app.last_account
    if not (accounts := check_account_exists(app.client, account_name, app.user)):
        raise ValueError(f'Account with account name {account_name} was not found.')
    return accounts[0]


def visualize_accounts(accounts):
    if not accounts:
        print('No account were found.')
        return
    order = ACCOUNTS_ORDER.copy()
    order.update(accounts[0])
    accounts[0] = order
    rows = [drop_sensitive_info(dict(account)) for account in accounts]
    print(tabulate.tabulate(rows, ACCOUNT_PROPERTIES))

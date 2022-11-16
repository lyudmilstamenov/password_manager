from getpass import getpass
from google.cloud import datastore
from utils import check_account_exists


def add_account(app):
    account_info = {}
    account_info['account_name'] = input('account name (This name must be unique per account.): ')
    account_info['app_name'] = input('app name []: ')
    account_info['login_url'] = input('login url []: ')
    account_info['username'] = input('username: ')
    account_info['email'] = input('email: ')
    account_info['notes'] = input('notes: ')
    account_info['password'] = getpass()
    if accounts:=check_account_exists(app.client,account_info['account_name']):
        raise ValueError(f'Account with account name {account_info["account_name"]} already exists.')
    account = datastore.Entity(app.client.key('Account'))
    account.update(account_info)
    app.client.put(account)
    print(f'Account with {account_info["account_name"]} was successfully created.')

def edit_account(app,account_name):
    if not (accounts:=check_account_exists(app.client,account_name)):
        raise ValueError(f'Account with account name {account_name} does not exist.')
    account = accounts[0]
    account_info = dict(account)
    pass


def delete_account(app):
    pass

def view_account(app,command):
    if command == '-all':
        return view_all_accounts(app)
    view_account_by_account_name(app,command)

def view_all_accounts(app):
    pass


def view_account_by_account_name(app, account_name):
    if accounts:=check_account_exists(app.client,account_name):
        visualize_account(accounts[0])
        return
    print(f'Account with account name {account_name} was not found.')




def visualize_account(account):
    # TODO
    print(dict(account.data))
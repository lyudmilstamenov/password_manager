import webbrowser
import pyperclip
from validators import url as url_validator
from google.cloud import datastore

from .account_helpers import update_account_info, init_account_info, retrieve_account_password, \
    retrieve_account_by_account_name

from .category_manager import add_account_to_category
from ..database.datastore_manager import retrieve_all_accounts_by_user
from ..database.base import save_entity
from ..common.utils import visualize_accounts
from ..common.account_consts import SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE, \
    SHOW_PWD_MESSAGE, DELETED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, \
    UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE, \
    URL_OPENED_MESSAGE, URL_NOT_VALID_MESSAGE


def add_account(app, owner_entity):
    account_info = init_account_info(app, owner_entity)
    account = datastore.Entity(app.client.key('Account'))
    save_entity(app.client, account, account_info)
    add_account_to_category(app, account_info['category'], account.key, owner_entity)
    app.last_account = account
    return SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE \
        .format(account_info['account_name'], app.user['name'])


def edit_account(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    print(UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE)
    account_info = update_account_info(app, account_name, owner_entity)
    save_entity(app.client, account, account_info)
    app.last_account = account
    return UPDATED_ACCOUNT_MESSAGE.format(account_info['account_name'], app.user['name'])


def delete_account(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    app.client.delete(account.key)
    app.last_account = None
    return DELETED_ACCOUNT_MESSAGE.format(account['account_name'], app.user['name'])


def view_account(app, command, owner_entity):
    if command == '-all':
        return view_all_accounts(app, owner_entity)
    return view_account_by_account_name(app, command, owner_entity)


def view_all_accounts(app, owner_entity):
    accounts = retrieve_all_accounts_by_user(app.client, owner_entity)
    visualize_accounts(owner_entity['name'], accounts)
    app.last_account = None
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def view_account_by_account_name(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    visualize_accounts(owner_entity['name'], [account])
    app.last_account = account
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def visualize_password(app, account_name, owner_entity):
    password = retrieve_account_password(app, account_name, owner_entity)
    return SHOW_PWD_MESSAGE.format(password, app.user['name'])


def copy_password(app, account_name, owner_entity):
    password = retrieve_account_password(app, account_name, owner_entity)
    pyperclip.copy(password)
    return COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['name'])


def open_url(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    url = account['login_url']
    if url and url_validator(url):
        webbrowser.open(url)
        return URL_OPENED_MESSAGE.format(app.user['name'])
    return URL_NOT_VALID_MESSAGE.format(app.user['name'])

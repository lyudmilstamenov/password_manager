"""
Provides functionalities for modifying accounts.
"""
import webbrowser
import pyperclip
from validators import url as url_validator

from src.database.datastore_manager import retrieve_all_accounts_by_user
from src.database.base import save_entity, create_entity
from src.common.utils import visualize_accounts
from src.common.account_consts import SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE, \
    SHOW_PWD_MESSAGE, DELETED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, \
    UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE, \
    URL_OPENED_MESSAGE, URL_NOT_VALID_MESSAGE

from ..helpers.account_helpers import update_account_info, init_account_info, \
    retrieve_account_password, retrieve_account_by_account_name
from .category_manager import add_account_to_category


def add_account(app, owner_entity):
    """
    Creates a new account with the given owner.
    :param app:
    :param owner_entity:
    :return:
    """
    account_info = init_account_info(app, owner_entity)
    account = create_entity(app, 'Account')
    save_entity(app.client, account, account_info)
    if account_info['category']:
        add_account_to_category(app, account_info['category'], account.key, owner_entity)
    app.last_accounts[owner_entity.key] = account
    return SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE \
        .format(account_info['account_name'], app.user['name'])


def edit_account(app, account_name, owner_entity):
    """
    Edits the account by name and owner.
    :param app:
    :param account_name:
    :param owner_entity:
    :return:
    """
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    print(UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE)
    account_info = update_account_info(app, account, owner_entity)
    save_entity(app.client, account, account_info)
    app.last_accounts[owner_entity.key] = account
    return UPDATED_ACCOUNT_MESSAGE.format(account_info['account_name'], app.user['name'])


def delete_account(app, account_name, owner_entity):
    """
    Deletes the account by name and owner.
    :param app:
    :param account_name:
    :param owner_entity:
    :return:
    """
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    app.client.delete(account.key)
    if owner_entity.key in app.last_accounts:
        del app.last_accounts[owner_entity.key]
    return DELETED_ACCOUNT_MESSAGE.format(account['account_name'], app.user['name'])


def view_account(app, command, owner_entity, filters=None):
    """
    Retrieves accounts based on the choice of the user.
    :param app:
    :param command:
    :param owner_entity:
    :param filters:
    :return:
    """
    if command == '-all':
        filters = filters if filters else {}
        return view_all_accounts(app, owner_entity, filters)
    return view_account_by_account_name(app, command, owner_entity)


def view_all_accounts(app, owner_entity, filters):
    """
    Retrieves all accounts by owner and filters them.
    :param app:
    :param owner_entity:
    :param filters:
    :return:
    """
    accounts = retrieve_all_accounts_by_user(app.client, owner_entity, filters=filters)
    visualize_accounts(owner_entity['name'], accounts)
    if owner_entity.key in app.last_accounts:
        del app.last_accounts[owner_entity.key]
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def view_account_by_account_name(app, account_name, owner_entity):
    """
    Retrieves an account by name and owner.
    :param app:
    :param account_name:
    :param owner_entity:
    :return:
    """
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    visualize_accounts(owner_entity['name'], [account])
    app.last_accounts[owner_entity.key] = account
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def visualize_password(app, account_name, owner_entity):
    """
    Retrieves the password of the account by account_name and returns it.
    :param app: App(contains the information about the current state of the programme)
    :param account_name:
    :param owner_entity: the owner(User/Organization) of the account
    :return str:
    """
    password = retrieve_account_password(app, account_name, owner_entity)
    return SHOW_PWD_MESSAGE.format(password, app.user['name'])


def copy_password(app, account_name, owner_entity):
    """
    Retrieves the password of the account by account_name
    and copies it to the clipboard.
    :param app: App(contains the information about the current state of the programme)
    :param account_name:
    :param owner_entity: the owner(User/Organization) of the account
    :return str:
    """
    password = retrieve_account_password(app, account_name, owner_entity)
    pyperclip.copy(password)
    return COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['name'])


def open_url(app, account_name, owner_entity):
    """
    Opens the url of the account by account_name.
    :param app: App(contains the information about the current state of the programme)
    :param account_name:
    :param owner_entity: the owner(User/Organization) of the account
    :return str: the appropriate message
    """
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    url = account['login_url']
    if url and url_validator(url):
        webbrowser.open(url)
        return URL_OPENED_MESSAGE.format(app.user['name'])
    return URL_NOT_VALID_MESSAGE.format(app.user['name'])

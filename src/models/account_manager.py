"""
Provides functionalities for modifying accounts.
"""
import urllib
import webbrowser
import pyperclip
from validators import url as url_validator

from src.database.datastore_manager import retrieve_all_accounts_by_user, retrieve_all_accounts_by_user_and_app
from src.database.base import save_entity, create_entity
from src.common.utils import visualize_accounts
from src.common.account_consts import SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE, \
    SHOW_PWD_MESSAGE, DELETED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, \
    UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE, \
    URL_OPENED_MESSAGE, URL_NOT_VALID_MESSAGE

from .account_helpers import update_account_info, init_account_info, retrieve_account_password, \
    retrieve_account_by_account_name
from .category_manager import add_account_to_category


def add_account(app, owner_entity):
    account_info = init_account_info(app, owner_entity)
    account = create_entity(app, 'Account')
    save_entity(app.client, account, account_info)
    add_account_to_category(app, account_info['category'], account.key, owner_entity)
    app.last_accounts[owner_entity.key] = account
    return SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE \
        .format(account_info['account_name'], app.user['name'])


def edit_account(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    print(UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE)
    account_info = update_account_info(app, account, owner_entity)
    save_entity(app.client, account, account_info)
    app.last_accounts[owner_entity.key] = account
    return UPDATED_ACCOUNT_MESSAGE.format(account_info['account_name'], app.user['name'])


def delete_account(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    app.client.delete(account.key)
    del app.last_accounts[owner_entity.key]
    return DELETED_ACCOUNT_MESSAGE.format(account['account_name'], app.user['name'])


def view_account(app, command, owner_entity, filters={}):
    if command == '-all':
        return view_all_accounts(app, owner_entity, filters)
    return view_account_by_account_name(app, command, owner_entity)


def view_all_accounts(app, owner_entity, filters={}):
    accounts = retrieve_all_accounts_by_user(app.client, owner_entity,filters=filters)
    visualize_accounts(owner_entity['name'], accounts)
    if owner_entity.key in app.last_accounts:
        del app.last_accounts[owner_entity.key]
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def view_account_by_account_name(app, account_name, owner_entity):
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


def url_fill_in(app, account_name, owner_entity):
    """
    Opens the url of the account by account_name and fills in the information.
    :param app: App(contains the information about the current state of the programme)
    :param account_name:
    :param owner_entity: the owner(User/Organization) of the account
    :return str: the appropriate message
    """

    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    url = account['login_url']

    if url and url_validator(url):
        pass
        # from selenium import webdriver
        # from selenium.webdriver.common.keys import Keys
        # from webdriver_manager.chrome import ChromeDriverManager
        #
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # chromedriver = 'C:\\chromedriver.exe'
        # browser = driver.Chrome(chromedriver)
        # browser.get('http:\\outlook.com\website.com')
        #
        # username = selenium.find_element_by_id("username")
        # password = selenium.find_element_by_id("password")
        #
        # username.send_keys("YourUsername")
        # password.send_keys("Pa55worD")
        #
        # selenium.find_element_by_name("submit").click()
        # # webbrowser.open(url)
        # return URL_OPENED_MESSAGE.format(app.user['name'])
    return URL_NOT_VALID_MESSAGE.format(app.user['name'])

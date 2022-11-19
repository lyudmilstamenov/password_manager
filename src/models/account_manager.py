import webbrowser
from getpass import getpass
import pyperclip
from validators import url as url_validator
from google.cloud import datastore

from ..common.erros import QuitError
from ..common.org_consts import ORG_NOT_FOUND_MESSAGE, WRONG_ORG_PWD_MESSAGE, ORG_PWD_MESSAGE
from ..common.utils import check_arguments_size
from .category_manager import add_account_to_category, update_category
from ..database.datastore_manager import check_account_exists, retrieve_all_accounts_by_user, check_org_exist
from ..database.base import save_entity
from ..common.utils import visualize_accounts
from ..common.account_consts import ACCOUNT_EXISTS_MESSAGE, SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE, \
    SHOW_PWD_MESSAGE, DELETED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, \
    UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE, ACCOUNT_NAME_INPUT_MESSAGE, \
    APP_NAME_INPUT_MESSAGE, LOGIN_URL_INPUT_MESSAGE, CATEGORY_INPUT_MESSAGE, \
    USERNAME_INPUT_MESSAGE, EMAIL_INPUT_MESSAGE, NOTES_INPUT_MESSAGE, PWD_INPUT_MESSAGE, \
    ACCOUNT_NOT_FOUND_MESSAGE, URL_OPENED_MESSAGE, URL_NOT_VALID_MESSAGE
from ..security.cryptography import encrypt, decrypt, check_password
from ..security.validation import validate_string_property, validate_email, \
    validate_url, validate_password, validate_entity_name


def add_account(app, owner_entity):
    account_info = populate_account_info(app, owner_entity)
    account_info['password'] = encrypt(account_info['password'], owner_entity['password'])
    account_info['owner'] = owner_entity.key
    if check_account_exists(app.client, account_info['account_name'], owner_entity):
        raise ValueError(ACCOUNT_EXISTS_MESSAGE.format(account_info["account_name"]))
    account = datastore.Entity(app.client.key('Account'))
    save_entity(app.client, account, account_info)
    add_account_to_category(app, account_info['category'], account.key, owner_entity)
    app.last_account = account
    return SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE \
        .format(account_info['account_name'], app.user['name'])


def edit_account(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    account_info = dict(account)
    print(UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE)
    new_account_info = populate_account_info(app, owner_entity, True)
    if new_account_info['category']:
        update_category(app, account_info['category'], new_account_info['category'], account.key, owner_entity)
    if new_account_info['password']:
        new_account_info['password'] = encrypt(new_account_info['password'], owner_entity['password'])
    for key, value in new_account_info.items():
        if value:
            account_info[key] = value
            continue
        if value == '-del':
            account[key] = ''

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
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    password = decrypt(account['password'], owner_entity['password'])  # decrypt
    app.last_account = account
    return SHOW_PWD_MESSAGE.format(password, app.user['name'])


def copy_password(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    password = decrypt(account['password'], owner_entity['password'])  # decrypt
    pyperclip.copy(password)
    app.last_account = account
    return COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['name'])


def open_url(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    url = account['login_url']
    if url and url_validator(url):
        webbrowser.open(url)
        return URL_OPENED_MESSAGE.format(app.user['name'])
    return URL_NOT_VALID_MESSAGE.format(app.user['name'])


def retrieve_account_by_account_name(app, account_name, owner):
    if app.last_account and account_name == app.last_account['account_name']:
        return app.last_account
    if not (accounts := check_account_exists(app.client, account_name, owner)):
        raise ValueError(ACCOUNT_NOT_FOUND_MESSAGE.format(account_name))
    return accounts[0]


def populate_account_info(app, owner_entity, can_be_empty=False):
    account_info = {
        'account_name': validate_entity_name(app, input(ACCOUNT_NAME_INPUT_MESSAGE),
                                             entity_kind='Account', owner_entity=owner_entity,
                                             can_be_empty=can_be_empty),
        'app_name': validate_string_property(input(APP_NAME_INPUT_MESSAGE),
                                             'app name', True),
        'login_url': validate_url(input(LOGIN_URL_INPUT_MESSAGE)),
        'category': validate_string_property(input(CATEGORY_INPUT_MESSAGE),
                                             'category', True),
        'username': validate_string_property(input(USERNAME_INPUT_MESSAGE),
                                             'username', can_be_empty),
        'email': validate_email(input(EMAIL_INPUT_MESSAGE), can_be_empty),
        'notes': input(NOTES_INPUT_MESSAGE),
        'password': validate_password(getpass(PWD_INPUT_MESSAGE),
                                      skip_validation=True, can_be_empty=can_be_empty)
    }
    account_info['pwd_length'] = len(account_info['password'])
    return account_info


def populate_org(app, commands):
    """
    Checks whether the commands contains -o. In this case retrieves the organization and returns it

    :param app App: App which holds the info about the user and the gcp client
    :param commands [str]: commands which are g=entered by the command prompt
    :return: (commands,organization), the following commands after retrieving the first two for the organization info
    and the found organization
    """
    if commands[0] != '-O':
        return commands, None
    check_arguments_size(commands, 3)
    org_name = commands[1]
    org = check_org_exist(app.client, org_name, app.user)
    if not org:
        raise ValueError(ORG_NOT_FOUND_MESSAGE.format(org_name, app.user['name']))
    org_pwd = getpass(ORG_PWD_MESSAGE)
    commands = [commands[2].upper()] + commands[3:]

    if not check_password(org_pwd, org[0]['password']):
        raise QuitError(WRONG_ORG_PWD_MESSAGE)
    return commands, org[0]

"""
Provides helper functions for modifying accounts.
"""
from getpass import getpass

from src.common.account_consts import ACCOUNT_NAME_INPUT_MESSAGE, \
    LOGIN_URL_INPUT_MESSAGE, CATEGORY_INPUT_MESSAGE, \
    APP_NAME_INPUT_MESSAGE, USERNAME_INPUT_MESSAGE, EMAIL_INPUT_MESSAGE, \
    NOTES_INPUT_MESSAGE, PWD_INPUT_MESSAGE, \
    ACCOUNT_EXISTS_MESSAGE, ACCOUNT_NOT_FOUND_MESSAGE, DELETE_PWD_MESSAGE
from src.database.datastore_manager import check_account_exists
from src.security.cryptography import encrypt, decrypt
from src.security.validation import validate_string_property, validate_email, \
    validate_url, validate_password, validate_entity_name
from .category_manager import update_category


def init_account_info(app, owner_entity):
    account_info = populate_account_info(app, owner_entity)
    account_info['password'] = encrypt(account_info['password'], owner_entity['password'])
    account_info['owner'] = owner_entity.key
    if check_account_exists(app.client, account_info['account_name'], owner_entity):
        raise ValueError(ACCOUNT_EXISTS_MESSAGE.format(account_info["account_name"]))
    return account_info


def update_account_info(app, account, owner_entity):
    account_info = dict(account)
    new_account_info = populate_account_info(app, owner_entity, True)
    if new_account_info['password'] == '-del':
        raise ValueError(DELETE_PWD_MESSAGE)
    if new_account_info['category']:
        update_category(app, account_info['category'],
                        new_account_info['category'], account.key, owner_entity)
    if new_account_info['password']:
        new_account_info['password'] = encrypt(new_account_info['password'],
                                               owner_entity['password'])
    for key, value in new_account_info.items():
        if value == '-del':
            account_info[key] = ''
            continue
        if value:
            account_info[key] = value
    return account_info


def retrieve_account_password(app, account_name, owner_entity):
    account = retrieve_account_by_account_name(app, account_name, owner_entity)
    app.last_account = account
    return decrypt(account['password'], owner_entity['password'])  # decrypt


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

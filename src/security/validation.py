import getpass
import re
from password_strength import PasswordStats, PasswordPolicy
from validators import url as url_validator, email as email_validator

from ..database.datastore_manager import check_user_exists, check_account_exists, check_org_exist
from ..common.account_consts import INVALID_PASSWORD_MESSAGE
from ..common.erros import QuitError, StopError
from ..common.consts import STRING_PROPERTY_VALIDATION_ERROR_MESSAGE, EMAIL_VALIDATION_ERROR_MESSAGE, \
    URL_VALIDATION_ERROR_MESSAGE, EXCEED_RETRIES_MESSAGE, WEAK_PASSWORD_MESSAGE, \
    MODERATE_PASSWORD_MESSAGE, STRONG_PASSWORD_MESSAGE, KIND_EXISTS_EXCEEDS_ENTRIES_MESSAGE, KIND_EXISTS_MESSAGE, \
    CHANGE_PASSWORD_MESSAGE


def validate_property(property_value, property_name, error_message, error_handler, can_be_empty, counter=0):
    if counter >= 5:
        raise QuitError(EXCEED_RETRIES_MESSAGE)
    if property_value.upper == 'EXIT':
        raise QuitError()
    if property_value.upper == 'STOP':
        raise StopError()
    if (can_be_empty and not property_value) or error_handler(property_value):
        return property_value
    print(error_message)
    property_value = input(f'{property_name}: ')
    return validate_property(property_value, property_name, error_message, error_handler, can_be_empty, counter + 1)


def is_string_property_valid(property_value):
    return bool(re.match(r'^[0-9a-zA-Z_.-]+$', property_value))


def validate_email(email, can_be_empty=False):
    return validate_property(email, 'email', EMAIL_VALIDATION_ERROR_MESSAGE,
                             email_validator, can_be_empty)


def validate_url(url, can_be_empty=True):
    return validate_property(url, 'login url', URL_VALIDATION_ERROR_MESSAGE,
                             url_validator, can_be_empty)


def validate_string_property(property_value, property_name, can_be_empty=False):
    return validate_property(property_value, property_name,
                             STRING_PROPERTY_VALIDATION_ERROR_MESSAGE.format(property_name),
                             is_string_property_valid, can_be_empty)


def validate_password(password, skip_validation=False, can_be_empty=False):
    if can_be_empty and not password:
        return password
    policy = PasswordPolicy.from_names(
        length=6,  # min length: 8
        uppercase=1,  # need min. 2 uppercase letters
        numbers=1,  # need min. 2 digits
        special=1,  # need min. 2 special characters
    )
    if (not skip_validation) and policy.test(password):
        print(INVALID_PASSWORD_MESSAGE)
        password = getpass.getpass('password: ')
        return validate_password(password, skip_validation)
    stats = PasswordStats(password)
    security_score = stats.strength() * 10
    if security_score < 4:
        print(WEAK_PASSWORD_MESSAGE.format(security_score))
    elif security_score < 7.8:
        print(MODERATE_PASSWORD_MESSAGE.format(security_score))
    else:
        print(STRONG_PASSWORD_MESSAGE.format(security_score))

    answer = input(CHANGE_PASSWORD_MESSAGE)
    if answer.upper() == 'YES':
        password = getpass.getpass('password: ')
        return validate_password(password, skip_validation)
    return password


def populate_fields(app, entity_kind):
    if entity_kind == 'Account':
        return 'Account', 'account name', \
               lambda value: check_account_exists(app.client, value, app.user)
    if entity_kind == 'User':
        return 'User', 'username', lambda value: check_user_exists(app.client, value)
    return 'Organization', 'organization name', \
           lambda value: check_org_exist(app.client, value, app.user)


def validate_entity_name(app, property_value, entity_kind, can_be_empty=False):
    kind_name, property_name, check_entity_exists = populate_fields(app, entity_kind)
    tries_count = 0
    while tries_count < 3:
        property_value = validate_string_property(property_value, property_name, can_be_empty)
        if not check_entity_exists(property_value):
            return property_value
        print(KIND_EXISTS_MESSAGE.format(kind_name, property_name))
        property_value = input(f'{property_name}: ')
        tries_count += 1

    if tries_count >= 3:
        raise QuitError(KIND_EXISTS_EXCEEDS_ENTRIES_MESSAGE.format(kind_name, property_name))

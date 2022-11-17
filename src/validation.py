import getpass
import re
from password_strength import PasswordStats, PasswordPolicy
from validators import url as url_validator, email as email_validator
from colorama import Fore

from common.erros import QuitError, StopError

from common.consts import STRING_PROPERTY_VALIDATION_ERROR_MESSAGE, EMAIL_VALIDATION_ERROR_MESSAGE, \
    URL_VALIDATION_ERROR_MESSAGE


def validate_property(property_value, property_name, error_message, error_handler, can_be_empty, counter=0):
    if counter >= 5:
        raise QuitError('You exceeded the allowed number of wrong entries.')
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


def validate_password(password, can_be_empty=False):
    if can_be_empty and not password:
        return password
    policy = PasswordPolicy.from_names(
        length=8,  # min length: 8
        uppercase=2,  # need min. 2 uppercase letters
        numbers=2,  # need min. 2 digits
        special=2,  # need min. 2 special characters
    )
    if policy.test(password):
        print(
            'Invalid password. The password should contain at least 8 characters, 2 uppercase letters, 2 digits and 2special characters.')
        password = getpass.getpass('password: ')
        return validate_password(password)
    stats = PasswordStats(password)
    security_score = stats.strength() * 10
    if security_score < 4:
        print(Fore.RED + f'The password is weak. Security score: {security_score}' + Fore.RESET)
    elif security_score < 7.8:
        print(Fore.YELLOW + f'The password is moderate. Security score: {security_score}' + Fore.RESET)
    else:
        print(Fore.GREEN + f'The password is strong. Security score: {security_score}' + Fore.RESET)

    answer = input('Do you want to change it?[yes/no]')
    if answer.upper() == 'YES':
        password = getpass.getpass('password: ')
        return validate_password(password)
    return password


def validate_entity_name(property_value, kind_name, property_name, check_entity_exists, can_be_empty=False,
                         number_of_tries=0):
    print(check_entity_exists)
    if number_of_tries >= 3:
        raise QuitError(
            f'{kind_name} with the same {property_name} already exists and you have exceeded the allowed number of wrong entries.')
    property_value = validate_string_property(property_value, property_name, can_be_empty)
    if check_entity_exists(property_value):
        print(f'{kind_name} with the same {property_name} already exists.')
        property_value = input(f'{property_name}: ')
        return validate_entity_name(property_value, kind_name, property_name, check_entity_exists, can_be_empty,
                                    number_of_tries + 1)
    return property_value

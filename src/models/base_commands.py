"""
Provides the functionalities of the base commands.
"""
from os import name, system
from password_generator import PasswordGenerator

import tabulate

from ..common.consts import HELP_TABLE_ORDER, HELP_TABLE_PROPERTIES, HELP_INFO_LIST, \
    INVALID_ARGUMENTS_MESSAGE, INVALID_PWD_LEN_MESSAGE, TOO_LARGE_PWD_LEN_MESSAGE


def visualize_help():
    """
    Presents the help information to the user.
    :return:
    """
    help_info = HELP_INFO_LIST
    order = HELP_TABLE_ORDER.copy()
    order.update(help_info[0])
    help_info[0] = order
    rows = help_info
    print(tabulate.tabulate(rows, HELP_TABLE_PROPERTIES))


def clear():
    """
    Clears the console.
    :return:
    """
    system('cls' if name == 'nt' else 'clear')


def generate_pwd(commands):
    """
    Generates a strong password.
    :param commands:
    :return:
    """
    try:
        length = 8 if not commands else int(commands[0])
    except Exception as exc:
        raise ValueError(INVALID_ARGUMENTS_MESSAGE) from exc
    if length < 4:
        raise ValueError(INVALID_PWD_LEN_MESSAGE)
    if length > 150:
        raise ValueError(TOO_LARGE_PWD_LEN_MESSAGE)

    pwd_generator = PasswordGenerator()
    pwd_generator.minlen = length
    pwd_generator.maxlen = length
    return pwd_generator.generate()

import string
import time
from os import name, system
import random

import tabulate

from ..common.consts import HELP_TABLE_ORDER, HELP_TABLE_PROPERTIES, HELP_INFO_LIST, \
    INVALID_ARGUMENTS_MESSAGE, INVALID_PWD_LEN_MESSAGE


def visualize_help():
    help_info = HELP_INFO_LIST
    order = HELP_TABLE_ORDER.copy()
    order.update(help_info[0])
    help_info[0] = order
    rows = help_info
    print(tabulate.tabulate(rows, HELP_TABLE_PROPERTIES))


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def generate_pwd(app, commands):
    try:
        length = 8 if not commands else int(commands[0])
    except Exception as exc:
        raise ValueError(INVALID_ARGUMENTS_MESSAGE) from exc
    if length <= 0:
        raise ValueError(INVALID_PWD_LEN_MESSAGE)
    random.seed(time.time() * 1000)
    all_symbols = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.sample(all_symbols, length))

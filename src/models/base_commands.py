from os import name, system

import tabulate

from ..common.consts import HELP_TABLE_ORDER, HELP_TABLE_PROPERTIES, HELP_INFO_LIST


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

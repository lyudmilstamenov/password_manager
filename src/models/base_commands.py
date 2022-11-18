from os import name, system

import tabulate

from ..common.consts import HELP_INFO, HELP_TABLE_ORDER, HELP_TABLE_PROPERTIES, HELP_INFO_LIST


def visualize_help():
    help = HELP_INFO_LIST
    order = HELP_TABLE_ORDER.copy()
    order.update(help[0])
    help[0] = order
    rows = help
    print(tabulate.tabulate(rows, HELP_TABLE_PROPERTIES))


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

"""
Provides basic functions used in different modules.
"""
import tabulate
from .account_consts import ACCOUNTS_ORDER, ACCOUNT_PROPERTIES, NOT_FOUND_ACCOUNTS_MESSAGE
from .category_consts import CATEGORY_PROPERTIES, CATEGORIES_ORDER, NOT_FOUND_CATEGORIES_MESSAGE
from .consts import NOT_ENOUGH_ARGUMENTS_MESSAGE


def visualize_accounts(owner_name, accounts):
    """
    Visualizes the information of the accounts
    :param owner_name: the name of the owner entity of the accounts
    :param accounts:
    :return:
    """
    if not accounts:
        print(NOT_FOUND_ACCOUNTS_MESSAGE)
        return
    order = ACCOUNTS_ORDER.copy()
    order.update(accounts[0])
    accounts[0] = order
    rows = [drop_sensitive_info(dict(account), owner_name) for account in accounts]
    print(tabulate.tabulate(rows, ACCOUNT_PROPERTIES))


def visualize_org(org):
    """
    Visualizes the information of the organization
    :param org:
    :return:
    """
    print('Organization name: ' + org['name'])
    print('Owner name: ' + org['owner'])
    print('Members: ' + ', '.join(org['users']))


def drop_sensitive_info(account, owner_name):
    """
    Deletes the sensitive information of the account.
    :param account:
    :param owner_name:
    :return:
    """
    account['password'] = '*' * account['pwd_length']
    account['owner'] = owner_name
    del account['pwd_length']
    return account


def visualize_categories(categories):
    """
    Presents the information of the given categories.
    :param categories:
    :return:
    """
    if not categories:
        print(NOT_FOUND_CATEGORIES_MESSAGE)
        return
    order = CATEGORIES_ORDER.copy()
    print(order)
    order.update(categories[0])
    categories[0] = order
    rows = [dict(category) for category in categories]
    print(tabulate.tabulate(rows, CATEGORY_PROPERTIES))


def check_arguments_size(commands, size=2):
    """
    Checks if enough arguments are given and raises an exception otherwise.
    :param commands:
    :param size:
    :return:
    """
    if len(commands) < size:
        raise ValueError(NOT_ENOUGH_ARGUMENTS_MESSAGE)


def get_owner(app, org):
    """
    Returns the owner of the accounts.
    By default if the user is logged in an organization, it uses the organization.
    :param app:
    :param org:
    :return:
    """
    if org:
        return org
    return app.user

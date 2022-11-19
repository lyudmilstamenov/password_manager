import tabulate
from .account_consts import ACCOUNTS_ORDER, ACCOUNT_PROPERTIES
from .category_consts import CATEGORY_PROPERTIES, CATEGORIES_ORDER
from .consts import NOT_ENOUGH_ARGUMENTS_MESSAGE


def visualize_accounts(owner_name, accounts):
    if not accounts:
        print('No account were found.')
        return
    order = ACCOUNTS_ORDER.copy()
    order.update(accounts[0])
    accounts[0] = order
    rows = [drop_sensitive_info(dict(account), owner_name) for account in accounts]
    print(tabulate.tabulate(rows, ACCOUNT_PROPERTIES))


def visualize_org(org):
    print('Organization name: ' + org['org_name'])
    print('Owner name: ' + org['owner'])
    print('Members: ' + ', '.join(org['users']))


def drop_sensitive_info(account, owner_name):
    account['password'] = '*' * account['pwd_length']
    account['owner'] = owner_name
    del account['pwd_length']
    return account


def visualize_categories(categories):
    if not categories:
        print('No categories were found.')
        return
    order = CATEGORIES_ORDER.copy()
    print(order)
    order.update(categories[0])
    categories[0] = order
    rows = [dict(category) for category in categories]
    print(tabulate.tabulate(rows, CATEGORY_PROPERTIES))


def check_arguments_size(commands, size=2):
    if len(commands) < size:
        raise ValueError(NOT_ENOUGH_ARGUMENTS_MESSAGE)


def get_owner(app, org):
    if org:
        return org
    else:
        return app.user
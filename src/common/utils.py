import tabulate
from common.consts import ACCOUNTS_ORDER, ACCOUNT_PROPERTIES, CATEGORY_PROPERTIES, CATEGORIES_ORDER






def visualize_accounts(owner_name, accounts):
    if not accounts:
        print('No account were found.')
        return
    order = ACCOUNTS_ORDER.copy()
    order.update(accounts[0])
    accounts[0] = order
    rows = [drop_sensitive_info(dict(account), owner_name) for account in accounts]
    print(tabulate.tabulate(rows, ACCOUNT_PROPERTIES))


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
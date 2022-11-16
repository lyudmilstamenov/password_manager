from consts import ACCOUNTS_ORDER, ACCOUNT_PROPERTIES
import tabulate


def check_user_exists(client, username):
    query = check_entity_exists(client, 'username', username, 'User')
    return list(query.fetch())


def check_category_exists(client, category_name, user):
    return check_account_or_category_exists(client, 'category_name', category_name, user, 'Category')


def retrieve_all_categories_by_user(client, user):
    return check_entity_exists(client, 'owner', user.key, 'Category')


def check_account_exists(client, account_name, user):
    return check_account_or_category_exists(client, 'account_name', account_name, user, 'Account')


def check_account_or_category_exists(client, key, value, user, kind):
    query = check_entity_exists(client, key, value, kind)
    query.add_filter('owner', '=', user.key)
    return list(query.fetch())


def check_entity_exists(client, filter_key, filter_value, kind):
    query = client.query(kind=kind)
    query.add_filter(filter_key, '=', filter_value)
    return query


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

def visualize_categories(categories,owner_name):
    pass
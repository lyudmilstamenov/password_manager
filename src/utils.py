def check_user_exists(client, username):
    query = check_entity_exists(client, 'username', username, 'User')
    return list(query.fetch())


def check_category_exists(client, category_name, user):
    return check_account_or_category_exists(client, 'category_name', category_name, user, 'Category')


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

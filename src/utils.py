def check_user_exists(client, username):
    return check_account_or_user_exists(client, 'username', username, 'User')


def check_account_exists(client, account_name):
    return check_account_or_user_exists(client, 'account_name', account_name, 'Account')


def check_account_or_user_exists(client, filter_key, filter_value, kind):
    query = client.query(kind=kind)
    query.add_filter(filter_key, "=", filter_value)
    return list(query.fetch())

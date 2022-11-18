from .base import create_query


def check_user_exists(client, username):
    return create_query(client, 'User', {'username': username})


def check_category_exists(client, category_name, user):
    return create_query(client, 'Category', {'owner': user.key, 'category_name': category_name})


def retrieve_all_categories_by_user(client, user):
    return create_query(client, 'Category', {'owner': user.key})


def retrieve_all_accounts_by_user(client, user):
    return create_query(client, 'Account', {'owner': user.key})


def check_account_exists(client, account_name, user):
    return create_query(client, 'Account', {'owner': user.key, 'account_name': account_name})


def check_org_exist(client, org_name, user):
    return create_query(client, 'Organization', {'users': user.key, 'org_name': org_name})


def check_owner_of_org(client, org_name, user):
    return create_query(client, 'Organization', {'owner': user.key, 'org_name': org_name})

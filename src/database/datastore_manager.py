"""
Provides functions for retrieving entities by specific parameters
"""

from .base import create_query


def check_user_exists(client, username):
    """
    Retrieves all users with name equal to username.
    :param client: the Google Datastore client
    :param username: username is unique per User,
     so the result have length <=1
    :return: list of account which meet the conditions
    """
    return create_query(client, 'User', {'name': username})


def check_category_exists(client, category_name, user):
    """
    Retrieves all categories by owner and category_name.
    :param client: the Google Datastore client
    :param category_name: category_name is unique per Category from a specific owner,
     so the result have length <=1
    :param user: User entity(the current logged in user)
    :return: list of categories which meet the conditions
    """
    return create_query(client, 'Category', {'owner': user.key, 'category_name': category_name})


def retrieve_all_categories_by_user(client, user):
    """
    Retrieves all categories by owner.
    :param client: the Google Datastore client
    :param user: User entity(the current logged in user)
    :return: list of categories which meet the conditions
    """
    return create_query(client, 'Category', {'owner': user.key})


def retrieve_all_accounts_by_user(client, owner, filters):
    """
    Retrieves all accounts by owner and filters the results using filters.
    :param client: the Google Datastore client
    :param owner: a datastore key of a User or an Organization
    :param filters: used to filter the list of accounts
    :return: list of accounts which meet the conditions
    """
    return create_query(client, 'Account', {'owner': owner.key} | filters)


def check_account_exists(client, account_name, owner):
    """
    Retrieves all accounts by owner and account_name.
    :param client: the Google Datastore client
    :param account_name: account_name is unique per Account, so the result have length <=1
    :param owner: a datastore key of a User or an Organization
    :return: list of accounts which meet the conditions
    """
    return create_query(client, 'Account', {'owner': owner.key, 'account_name': account_name})


def check_org_exist(client, org_name, user):
    """
    Retrieves all organizations with org_name as a name and
    the user is the owner of the organization or the user is a member.
    :param client: the Google Datastore client
    :param org_name: org_name is unique per Organization, so the result have length <=1
    :param user: User entity(the current logged in user)
    :return: list of organizations which meet the conditions
    """
    # TODO maybe change to User get by key and check orgs:org_name
    if orgs := check_owner_of_org(client, org_name, user):
        return orgs
    return check_member_of_org(client, org_name, user)


def check_member_of_org(client, org_name, user):
    """
    Retrieves all organizations  with org_name as a name
    and the user is a member of the organization.
    :param client: the Google Datastore client
    :param org_name: org_name is unique per Organization, so the result have length <=1
    :param user: User entity(the current logged in user)
    :return: list of organizations which meet the conditions
    """
    return create_query(client, 'Organization', {'users': user.key, 'name': org_name})


def check_owner_of_org(client, org_name, user):
    """
    Retrieves all organizations with org_name as a name
    and the user is a member of the organization.
    :param client: the Google Datastore client
    :param org_name: org_name is unique per Organization, so the result have length <=1
    :param user: User entity(the current logged in user)
    :return: list of organizations which meet the conditions
    """
    return create_query(client, 'Organization', {'owner': user.key, 'name': org_name})

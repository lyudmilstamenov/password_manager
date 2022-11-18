from google.cloud import datastore

from ..common.consts import USER_NOT_FOUND_MESSAGE, ENTER_COMMAND_WITH_USER_MESSAGE
from ..common.erros import QuitError
from ..common.org_consts import USERS_NOT_FOUND_MESSAGE, \
    SUCCESSFULLY_CREATED_ORG_MESSAGE, DELETED_ORG_MESSAGE, \
    ADDED_USER_TO_ORG_MESSAGE, REMOVED_USER_FROM_ORG_MESSAGE, REMOVE_YOURSELF_FROM_ORG_MESSAGE, \
    ORG_NOT_DELETED_MESSAGE, REMOVE_ORG_QUESTION_MESSAGE
from ..common.utils import visualize_org
from ..database.base import save_entity
from ..database.datastore_manager import check_user_exists, check_owner_of_org
from ..security.validation import validate_entity_name


def add_org_to_user(client, user, org):
    user_info = dict(user)
    user_info['orgs'].append(org.key)
    save_entity(client, user, user_info)


def create_organization(app, users):
    org_name = validate_entity_name(app, (input('organization name: ')), entity_kind='Organization')
    not_found_users = []
    users_keys = []
    found_users = []
    org = datastore.Entity(app.client.key('Organization'))
    for username in users:
        user = check_user_exists(app.client, username)
        if not user:
            not_found_users.append(username)
            continue
        users_keys.append(user[0].key)
        found_users.append(user[0])

    org_info = {'org_name': org_name, 'users': users_keys, 'owner': app.user.key}
    save_entity(app.client, org, org_info)
    for user in found_users:
        add_org_to_user(app.client, user, org)
    if not_found_users:
        return USERS_NOT_FOUND_MESSAGE.format(', '.join(not_found_users)) \
               + SUCCESSFULLY_CREATED_ORG_MESSAGE.format(org_name, app.user['username'])
    return SUCCESSFULLY_CREATED_ORG_MESSAGE.format(org_name, app.user['username'])


def add_user_organization(app, org_name, username):
    org = retrieve_org(app.client, app.user, org_name)
    org_info = dict(org)
    users = check_user_exists(app.client, username)

    if not users:
        raise ValueError(USER_NOT_FOUND_MESSAGE.format(username))
    org_info['users'].append(users[0].key)
    add_org_to_user(app.client, users[0], org)
    save_entity(app.client, org, org_info)

    return ADDED_USER_TO_ORG_MESSAGE.format(username, org_name, app.user['username'])


def delete_org_from_user(client, org, user):
    user_info = dict(user)
    user_info['orgs'].remove(org.key)
    save_entity(client, user, user_info)


def drop_sensitive_info_from_org(app, org_info):
    usernames = []
    for user_key in org_info['users']:
        usernames.append(app.client.get(user_key)['username'])
    org_info['users'] = usernames
    org_info['owner'] = app.client.get(org_info['owner'])['username']
    return org_info


def view_org(app, org_name):
    org = retrieve_org(app.client, app.user, org_name)
    visualize_org(drop_sensitive_info_from_org(app, dict(org)))
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['username'])


def remove_user_from_organization(app, org_name, username):
    if username == app.user['username']:
        raise QuitError(REMOVE_YOURSELF_FROM_ORG_MESSAGE)

    org = retrieve_org(app.client, app.user, org_name)
    org_info = dict(org)
    users = check_user_exists(app.client, username)

    if not users:
        raise ValueError(USER_NOT_FOUND_MESSAGE.format(username))
    org_info['users'].remove(users[0].key)
    delete_org_from_user(app.client, org, users[0])
    save_entity(app.client, org, org_info)

    return REMOVED_USER_FROM_ORG_MESSAGE.format(username, org_name, app.user['username'])


def remove_all_users_from_org(app, org):
    for user in org['users']:
        delete_org_from_user(app.client, org, user)


def delete_org(app, org_name):
    org = retrieve_org(app.client, org_name, app.user)
    if org['users']:
        answer = input(REMOVE_ORG_QUESTION_MESSAGE)
        if answer.upper() != 'YES':
            return ORG_NOT_DELETED_MESSAGE.format(app.user['username'])
        remove_all_users_from_org(app, org)
    app.client.delete(org.key)
    return DELETED_ORG_MESSAGE.format(org['org_name'], app.user['username'])


def retrieve_org(client, user, org_name):
    orgs = check_owner_of_org(client, org_name, user)
    if not orgs:
        raise QuitError('You are not owner of an organization with the same name.')
    return orgs[0]

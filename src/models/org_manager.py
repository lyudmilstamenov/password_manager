from google.cloud import datastore

from .org_helpers import init_org_info, drop_sensitive_info_from_org, \
    remove_all_users_from_org, retrieve_org, \
    delete_org_from_user
from ..common.consts import USER_NOT_FOUND_MESSAGE, ENTER_COMMAND_WITH_USER_MESSAGE
from ..common.erros import QuitError
from ..common.org_consts import USERS_NOT_FOUND_MESSAGE, \
    SUCCESSFULLY_CREATED_ORG_MESSAGE, DELETED_ORG_MESSAGE, \
    ADDED_USER_TO_ORG_MESSAGE, REMOVED_USER_FROM_ORG_MESSAGE, REMOVE_YOURSELF_FROM_ORG_MESSAGE, \
    ORG_NOT_DELETED_MESSAGE, REMOVE_ORG_QUESTION_MESSAGE, NO_ORGS_MESSAGE, ALL_ORGS_MESSAGE
from ..common.utils import visualize_org
from ..database.base import save_entity
from ..database.datastore_manager import check_user_exists


def add_org_to_user(client, user, org):
    user_info = dict(user)
    user_info['orgs'].append(org.key)
    save_entity(client, user, user_info)


def create_organization(app, users):
    org_info, found_users, not_found_users = init_org_info(app, users)
    org = datastore.Entity(app.client.key('Organization'))
    save_entity(app.client, org, org_info)
    for user in found_users:
        add_org_to_user(app.client, user, org)
    add_org_to_user(app.client, app.user, org)
    if not_found_users:
        return USERS_NOT_FOUND_MESSAGE.format(', '.join(not_found_users)) \
               + SUCCESSFULLY_CREATED_ORG_MESSAGE.format(org_info['name'], app.user['name'])
    return SUCCESSFULLY_CREATED_ORG_MESSAGE.format(org_info['name'], app.user['name'])


def add_user_to_organization(app, org_name, username):
    org = retrieve_org(app.client, app.user, org_name)
    org_info = dict(org)
    users = check_user_exists(app.client, username)

    if not users:
        raise ValueError(USER_NOT_FOUND_MESSAGE.format(username))
    org_info['users'].append(users[0].key)
    add_org_to_user(app.client, users[0], org)
    save_entity(app.client, org, org_info)

    return ADDED_USER_TO_ORG_MESSAGE.format(username, org_name, app.user['name'
                                                                         ''])


def view_all_orgs(app):
    orgs = [app.client.get(org_key) for org_key in app.user['orgs']]
    if not orgs:
        return NO_ORGS_MESSAGE.format(app.user['name'])
    orgs_string = ', '.join([org['name'] for org in orgs if org])
    return ALL_ORGS_MESSAGE + orgs_string + ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def view_org(app, org_name):
    org = retrieve_org(app.client, app.user, org_name)
    visualize_org(drop_sensitive_info_from_org(app, dict(org)))
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def remove_user_from_organization(app, org_name, username):
    if username == app.user['name']:
        raise QuitError(REMOVE_YOURSELF_FROM_ORG_MESSAGE)

    org = retrieve_org(app.client, app.user, org_name)
    org_info = dict(org)
    users = check_user_exists(app.client, username)

    if not users:
        raise ValueError(USER_NOT_FOUND_MESSAGE.format(username))
    org_info['users'].remove(users[0].key)
    delete_org_from_user(app.client, org, users[0])
    save_entity(app.client, org, org_info)

    return REMOVED_USER_FROM_ORG_MESSAGE.format(username, org_name, app.user['name'])


def delete_org(app, org_name):
    org = retrieve_org(app.client, app.user, org_name)
    if org['users']:
        answer = input(REMOVE_ORG_QUESTION_MESSAGE)
        if answer.upper() != 'YES':
            return ORG_NOT_DELETED_MESSAGE.format(app.user['name'])
        remove_all_users_from_org(app, org)
    app.client.delete(org.key)
    return DELETED_ORG_MESSAGE.format(org['name'], app.user['name'])

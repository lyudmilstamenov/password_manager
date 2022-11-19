from getpass import getpass

from ..common.account_consts import PWD_INPUT_MESSAGE
from ..common.erros import QuitError
from ..common.org_consts import NOT_OWNER_OF_ORG_MESSAGE
from ..database.base import save_entity
from ..database.datastore_manager import check_user_exists, check_owner_of_org
from ..security.cryptography import get_hashed_password
from ..security.validation import validate_entity_name, validate_password


def init_org_info(app, users):
    org_name = validate_entity_name(app, (input('organization name: ')), entity_kind='Organization')
    org_pwd = validate_password(getpass(PWD_INPUT_MESSAGE))
    not_found_users = []
    users_keys = []
    found_users = []

    for username in users:
        user = check_user_exists(app.client, username)
        if not user:
            not_found_users.append(username)
            continue
        users_keys.append(user[0].key)
        found_users.append(user[0])

    return {
               'name': org_name,
               'password': get_hashed_password(org_pwd),
               'users': users_keys,
               'owner': app.user.key
           }, found_users, not_found_users


def drop_sensitive_info_from_org(app, org_info):
    usernames = []
    for user_key in org_info['users']:
        usernames.append(app.client.get(user_key)['name'])
    org_info['users'] = usernames
    org_info['owner'] = app.client.get(org_info['owner'])['name']
    return org_info


def remove_all_users_from_org(app, org):
    for user_key in org['users']:
        delete_org_from_user(app.client, org, app.client.get(user_key))


def delete_org_from_user(client, org, user):
    user_info = dict(user)
    user_info['orgs'].remove(org.key)
    save_entity(client, user, user_info)


def retrieve_org(client, user, org_name):
    orgs = check_owner_of_org(client, org_name, user)
    if not orgs:
        raise QuitError(NOT_OWNER_OF_ORG_MESSAGE)
    return orgs[0]

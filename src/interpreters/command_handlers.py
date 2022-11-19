from getpass import getpass

from ..common.org_consts import ORG_NOT_FOUND_MESSAGE, WRONG_ORG_PWD_MESSAGE, ORG_PWD_MESSAGE
from ..database.datastore_manager import check_org_exist
from ..security.cryptography import check_password
from ..models.base_commands import visualize_help, clear
from ..models import user_manager
from ..models.account_manager import add_account, edit_account, \
    delete_account, view_account, copy_password, \
    visualize_password, open_url
from ..models.category_manager import delete_category, \
    view_all_accounts_by_category, view_all_categories
from ..models.org_manager import create_organization, \
    add_user_to_organization, remove_user_from_organization, delete_org, \
    view_org, view_all_orgs
from ..common.erros import StopError, QuitError
from ..common.account_consts import NO_LAST_ACCOUNT_MESSAGE
from ..common.consts import HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, \
    NOT_ENOUGH_ARGUMENTS_MESSAGE, \
    INVALID_ARGUMENTS_MESSAGE, INVALID_COMMAND_MESSAGE, ONLY_LOGIN_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE
from ..common.utils import check_arguments_size, get_owner


def login_or_signup(commands, app):
    if commands[0] == 'LOGIN':
        return user_manager.login(app)
    if commands[0] == 'SIGNUP':
        return user_manager.signup(app)
    return ONLY_LOGIN_MESSAGE + HELP_MESSAGE + '\n$'


def handle_category_commands(commands, app):
    commands, org = populate_org(app, commands)
    owner_entity = get_owner(app, org)
    if commands[0] == '-ALL':
        return view_all_categories(app, owner_entity)
    if len(commands) < 2:
        raise ValueError(NOT_ENOUGH_ARGUMENTS_MESSAGE)
    if commands[0] == '-RM':
        return delete_category(app, commands[1], owner_entity)
    raise ValueError(INVALID_ARGUMENTS_MESSAGE)


def handle_user_commands(commands, app):
    check_arguments_size(commands)
    if commands[0] == 'ACCOUNT':
        return handle_account_commands(commands[1:], app)
    if commands[0] == 'ORG':
        return handle_org_commands(commands[1:], app)
    if commands[0] == 'CATEGORY':
        return handle_category_commands(commands[1:], app)
    raise ValueError(INVALID_COMMAND_MESSAGE)


def handle_account_commands(commands, app):
    commands, org = populate_org(app, commands)
    owner_entity = get_owner(app, org)
    if commands[0] == 'ADD':
        return add_account(app, owner_entity)
    check_arguments_size(commands)
    if commands[0] == 'CAT':
        return view_all_accounts_by_category(app, commands[1], owner_entity)
    if commands[0] == 'EDIT':
        return edit_account(app, commands[1], owner_entity)
    if commands[0] == '-RM':
        return delete_account(app, commands[1], owner_entity)
    return handle_account_view_commands(commands, app, owner_entity)


def handle_account_view_commands(commands, app, owner_entity):
    if commands[1] == '-last' and not app.last_account:
        raise ValueError(NO_LAST_ACCOUNT_MESSAGE)
    if commands[1] == '-last':
        commands[1] = app.last_account['account_name']
    if commands[0] == 'VIEW':
        return view_account(app, commands[1], owner_entity)
    if commands[0] == 'COPY-PWD':
        return copy_password(app, commands[1], owner_entity)
    if commands[0] == 'PWD':
        return visualize_password(app, commands[1], owner_entity)
    if commands[0] == 'URL':
        return open_url(app, commands[1], owner_entity)
    raise ValueError(INVALID_ARGUMENTS_MESSAGE)


def handle_org_commands(commands, app):
    if commands[0] == 'ALL':
        return view_all_orgs(app)
    if commands[0] == 'CREATE':
        return create_organization(app, commands[1:])
    check_arguments_size(commands)
    if commands[0] == 'DELETE':
        return delete_org(app, commands[1])
    if commands[0] == 'VIEW':
        return view_org(app, commands[1])
    check_arguments_size(commands, 3)
    if commands[0] == 'ADD':
        return add_user_to_organization(app, commands[1], commands[2])
    if commands[0] == 'REMOVE':
        return remove_user_from_organization(app, commands[1], commands[2])
    raise ValueError(INVALID_ARGUMENTS_MESSAGE)


def handle_base_commands(app, command):
    if command == 'CLEAR':
        clear()
        return '$: ' if not app.user \
            else ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
    if command == 'HELP':
        visualize_help()
        return '$: ' if not app.user \
            else ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
    if command == 'LOGOUT':
        app.user = None
        app.last_account = None
        return LOGIN_OR_SIGNUP_MESSAGE
    raise StopError()


def populate_org(app, commands):
    """
    Checks whether the commands contains -o. In this case retrieves the organization and returns it

    :param app App: App which holds the info about the user and the gcp client
    :param commands [str]: commands which are g=entered by the command prompt
    :return: (commands,organization), the following commands after
    retrieving the first two for the organization info
    and the found organization
    """
    if commands[0] != '-O':
        return commands, None
    check_arguments_size(commands, 3)
    org_name = commands[1]
    org = check_org_exist(app.client, org_name, app.user)
    if not org:
        raise ValueError(ORG_NOT_FOUND_MESSAGE.format(org_name, app.user['name']))
    org_pwd = getpass(ORG_PWD_MESSAGE)
    commands = [commands[2].upper()] + commands[3:]

    if not check_password(org_pwd, org[0]['password']):
        raise QuitError(WRONG_ORG_PWD_MESSAGE)
    return commands, org[0]
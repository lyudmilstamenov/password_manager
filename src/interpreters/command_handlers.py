from getpass import getpass

from ..common.org_consts import ORG_NOT_FOUND_MESSAGE, WRONG_ORG_PWD_MESSAGE, ORG_PWD_MESSAGE, NO_LAST_ORG_MESSAGE
from ..database.datastore_manager import check_org_exist
from ..security.cryptography import check_password
from ..server.helpers.base_helpers import visualize_help, clear, generate_pwd
from ..server.managers import user_manager
from ..server.managers.account_manager import add_account, edit_account, \
    delete_account, view_account, copy_password, \
    visualize_password, open_url
from ..server.managers.category_manager import delete_category, \
    view_all_accounts_by_category, view_all_categories
from ..server.managers.org_manager import create_organization, \
    add_user_to_organization, remove_user_from_organization, delete_org, \
    view_org, view_all_orgs
from ..common.erros import StopError, QuitError
from ..common.account_consts import NO_LAST_ACCOUNT_MESSAGE
from ..common.consts import HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, \
    NOT_ENOUGH_ARGUMENTS_MESSAGE, \
    INVALID_ARGUMENTS_MESSAGE, INVALID_COMMAND_MESSAGE, ONLY_LOGIN_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, GENERATE_PWD_MESSAGE
from ..common.utils import check_arguments_size, get_owner


def login_or_signup(commands, app):
    handlers = {
        'LOGIN': lambda: user_manager.login(app),
        'SIGNUP': lambda: user_manager.signup(app),
    }
    return handlers.get(commands[0], lambda: ONLY_LOGIN_MESSAGE + HELP_MESSAGE + '\n$ ')()


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
    handlers = {
        'ACCOUNT': lambda: handle_account_commands(commands[1:], app),
        'ORG': lambda: handle_org_commands(commands[1:], app),
        'CATEGORY': lambda: handle_category_commands(commands[1:], app)
    }
    if commands[0] in handlers:
        return handlers[commands[0]]()
    raise ValueError(INVALID_COMMAND_MESSAGE)


def handle_account_commands(commands, app):
    commands, org = populate_org(app, commands)
    owner_entity = get_owner(app, org)
    if commands[0] == 'ADD':
        return add_account(app, owner_entity)
    check_arguments_size(commands)
    handlers = {
        'CAT': lambda: view_all_accounts_by_category(app, commands[1], owner_entity),
        'EDIT': lambda: edit_account(app, commands[1], owner_entity),
        '-RM': lambda: delete_account(app, commands[1], owner_entity),
    }
    return handlers.get(commands[0], lambda: handle_account_view_commands(commands, app, owner_entity))()


def handle_account_view_commands(commands, app, owner_entity):
    parameter = extract_account_name(app, commands[1], owner_entity)
    handlers = {
        'VIEW': lambda: view_account(app, parameter, owner_entity),
        'COPY-PWD': lambda: copy_password(app, parameter, owner_entity),
        'PWD': lambda: visualize_password(app, parameter, owner_entity),
        'URL': lambda: open_url(app, parameter, owner_entity),
        'VIEW-BY-APP': lambda: view_account(app, '-all', owner_entity, filters={'app_name': parameter})
    }
    if commands[0] in handlers:
        return handlers[commands[0]]()
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


def handle_base_commands(app, commands):
    if commands[0] == 'CLEAR':
        clear()
        return '$: ' if not app.user \
            else ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
    if commands[0] == 'HELP':
        visualize_help()
        return '$: ' if not app.user \
            else ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
    if commands[0] == 'LOGOUT':
        app.user = None
        return LOGIN_OR_SIGNUP_MESSAGE
    if commands[0] == 'STOP':
        raise StopError()
    if commands[0] == 'GEN':
        return GENERATE_PWD_MESSAGE.format(generate_pwd(commands[1:]), '' if not app.user else app.user['name'])
    raise QuitError(INVALID_COMMAND_MESSAGE)


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
    commands = [commands[2].upper()] + commands[3:]

    if app.last_org and org_name in ['-last', app.last_org['name']]:
        return commands, app.last_org
    if org_name == '-last' and not app.last_org:
        raise ValueError(NO_LAST_ORG_MESSAGE)

    org = check_org_exist(app.client, org_name)
    if not org:
        raise ValueError(ORG_NOT_FOUND_MESSAGE.format(org_name))
    org_pwd = getpass(ORG_PWD_MESSAGE)

    if not check_password(org_pwd, org[0]['password']):
        raise QuitError(WRONG_ORG_PWD_MESSAGE)
    app.last_org = org[0]
    return commands, org[0]


def extract_account_name(app, command, owner_entity):
    if command != '-last':
        return command
    if not (owner_entity.key in app.last_accounts):
        raise ValueError(NO_LAST_ACCOUNT_MESSAGE.format(owner_entity['name']))
    return app.last_accounts[owner_entity.key]['account_name']

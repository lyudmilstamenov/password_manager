from common.account_consts import NO_LAST_ACCOUNT_MESSAGE
from models import user_manager
from app import App
from common.consts import COMMANDS, HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, HELP_INFO, NOT_ENOUGH_ARGUMENTS_MESSAGE, \
    INVALID_ARGUMENTS_MESSAGE, INVALID_COMMAND_MESSAGE, ONLY_LOGIN_MESSAGE, STOP_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, QUIT_MESSAGE
from models.account_manager import add_account, edit_account, delete_account, view_account, copy_password, \
    visualize_password, open_url
from os import system, name

from models.category_manager import delete_category, view_all_accounts_by_category, view_all_categories
from common.erros import StopError, QuitError


def console():
    app = App()
    key = app.client.key('User', 5632499082330112)
    app.user = app.client.get(key)
    print(HELP_MESSAGE)
    input_message = LOGIN_OR_SIGNUP_MESSAGE
    command = None
    while command != 'STOP':
        input_string = input(input_message)
        input_list = input_string.split()
        commands = [cmd.upper() for cmd in input_list[0:2]] + input_list[2:]
        print(commands)
        command = commands[0]
        if command not in COMMANDS:
            print(INVALID_COMMAND_MESSAGE + HELP_MESSAGE)
            continue
        if command == 'CLEAR':
            clear()
            continue
        if command == 'HELP':
            visualize_help()
            continue
        if command == 'LOGOUT':
            app.user = None
            app.last_account = None
            input_message = LOGIN_OR_SIGNUP_MESSAGE
            continue
        if not app.user:
            input_message = login_or_signup(commands, app)
            continue
        try:
            input_message = handle_user_commands(commands, app)
        except ValueError as exc:
            input_message = str(exc) + HELP_MESSAGE + ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['username'])
            continue
        except StopError:
            print(STOP_MESSAGE)
            break
        except QuitError as exc:
            input_message = QUIT_MESSAGE + str(exc) + HELP_MESSAGE + ENTER_COMMAND_WITH_USER_MESSAGE.format(
                app.user['username'])


def login_or_signup(commands, app):
    if commands[0] == 'LOGIN':
        return user_manager.login(app)
    if commands[0] == 'SIGNUP':
        return user_manager.signup(app)
    return ONLY_LOGIN_MESSAGE + HELP_MESSAGE + '\n$'


def handle_category_commands(commands, app):
    if commands[0] == '-ALL':
        return view_all_categories(app)
    if len(commands) < 2:
        raise ValueError(NOT_ENOUGH_ARGUMENTS_MESSAGE)
    if commands[0] == '-RM':
        return delete_category(app, commands[1])
    raise ValueError(INVALID_ARGUMENTS_MESSAGE)


def handle_user_commands(commands, app):
    if commands[0] == 'ACCOUNT':
        return handle_account_commands(commands[1:], app)
    if commands[0] == 'ORG':
        return handle_org_commands(commands[1:], app)
    if commands[0] == 'CATEGORY':
        return handle_category_commands(commands[1:], app)
    raise ValueError(INVALID_COMMAND_MESSAGE)


def handle_account_commands(commands, app):
    if commands[0] == 'ADD':
        return add_account(app)
    if len(commands) < 2:
        raise ValueError(NOT_ENOUGH_ARGUMENTS_MESSAGE)
    if commands[0] == 'CAT':
        return view_all_accounts_by_category(app, commands[1])
    if commands[0] == 'EDIT':
        return edit_account(app, commands[1])
    if commands[0] == '-RM':
        return delete_account(app, commands[1])
    if commands[1] == '-last' and not app.last_account:
        raise ValueError(NO_LAST_ACCOUNT_MESSAGE)
    if commands[1] == '-last':
        commands[1] = app.last_account['account_name']
    if commands[0] == 'VIEW':
        return view_account(app, commands[1])
    if commands[0] == 'COPY-PWD':
        return copy_password(app, commands[1])
    if commands[0] == 'PWD':
        return visualize_password(app, commands[1])
    if commands[0] == 'URL':
        return open_url(app, commands[1])
    raise ValueError(INVALID_ARGUMENTS_MESSAGE)


def handle_org_commands(commands, app):
    pass


def visualize_help():
    print(HELP_INFO)


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == '__main__':
    console()

from ..app import App
from ..common.erros import StopError, QuitError

from ..common.consts import COMMANDS, HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, INVALID_COMMAND_MESSAGE, STOP_MESSAGE, \
    ENTER_COMMAND_WITH_USER_MESSAGE, QUIT_MESSAGE, BASE_COMMANDS, BASE_ERROR_MESSAGE
from .command_handlers import handle_base_commands, login_or_signup, handle_user_commands


def run():
    app = App()
    print(HELP_MESSAGE)
    input_message = LOGIN_OR_SIGNUP_MESSAGE
    command = None
    while command != 'STOP':
        commands = extract_commands(input_message)
        try:
            input_message = handle_commands(app, commands)
        except StopError:
            break
        except ValueError as exc:
            input_message = BASE_ERROR_MESSAGE.format(str(exc), app.user['name'])
            continue
        except QuitError as exc:
            input_message = QUIT_MESSAGE + BASE_ERROR_MESSAGE.format(str(exc), app.user['name'])
    print(STOP_MESSAGE)


def handle_commands(app, commands):
    command = commands[0]
    if command not in COMMANDS:
        print(INVALID_COMMAND_MESSAGE + HELP_MESSAGE)
        return '$: ' if not app.user \
            else ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
    if command in BASE_COMMANDS:
        return handle_base_commands(app, command)
    if not app.user:
        return login_or_signup(commands, app)

    return handle_user_commands(commands, app)


def extract_commands(input_message):
    input_string = input(input_message)
    input_list = input_string.split()
    return [cmd.upper() for cmd in input_list[0:2]] + input_list[2:]

import sys

from ..app import App
from ..common.erros import StopError, QuitError, ForbiddenOperationError

from ..common.consts import COMMANDS, HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, INVALID_COMMAND_MESSAGE, STOP_MESSAGE, \
    QUIT_MESSAGE, BASE_COMMANDS, BASE_ERROR_MESSAGE, EMPTY_COMMAND_MESSAGE, ALREADY_LOGGED_IN_ERROR_MESSAGE, \
    FORBIDDEN_OPERATION_MESSAGE, UNKNOWN_ERROR_MESSAGE
from .command_handlers import handle_base_commands, login_or_signup, handle_user_commands


def run():
    app = App()
    app.user = app.client.get(app.client.key('User', 5644004762845184))
    print(HELP_MESSAGE)
    input_message = LOGIN_OR_SIGNUP_MESSAGE
    command = None
    while command != 'STOP':
        commands = extract_commands(input_message)
        try:
            input_message = handle_commands(app, commands)
        except StopError:
            break


def catch_base_errors(func):
    """
    Processes the raised exceptions and returns input message.
    :param func: handler to be executed
    :return: message
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            sys.stderr.write(str(exc))
            return BASE_ERROR_MESSAGE.format(args[0].user['name'] if args[0].user else '')
        except QuitError as exc:
            sys.stderr.write(QUIT_MESSAGE + str(exc))
            return BASE_ERROR_MESSAGE.format(args[0].user['name'])
        except ForbiddenOperationError as exc:
            sys.stderr.write(FORBIDDEN_OPERATION_MESSAGE + str(exc))
            return BASE_ERROR_MESSAGE.format(args[0].user['name'])
        except StopError:
            sys.stderr.write(STOP_MESSAGE)
            raise
        except Exception as exc:
            sys.stderr.write(UNKNOWN_ERROR_MESSAGE)
            print(exc)
            return BASE_ERROR_MESSAGE.format(args[0].user['name'])

    return inner


@catch_base_errors
def handle_commands(app, commands):
    if not commands:
        raise ValueError(EMPTY_COMMAND_MESSAGE)
    command = commands[0]
    if command not in COMMANDS:
        raise ValueError(INVALID_COMMAND_MESSAGE)
    if command in BASE_COMMANDS:
        return handle_base_commands(app, commands)
    if not app.user:
        return login_or_signup(commands, app)
    if commands[0] == 'LOGIN':
        raise ForbiddenOperationError(ALREADY_LOGGED_IN_ERROR_MESSAGE)
    return handle_user_commands(commands, app)


def extract_commands(input_message):
    """
    Extracts the commands from the entered string.
    :param input_message: str of commands
    :return: list of commands
    """
    input_string = input(input_message)
    input_list = input_string.split()
    return [cmd.upper() for cmd in input_list[0:2]] + input_list[2:]

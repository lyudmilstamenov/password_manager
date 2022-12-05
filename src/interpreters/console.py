import sys

from google.cloud.datastore import Key

from ..app import App
from ..common.erros import StopError, QuitError

from ..common.consts import COMMANDS, HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, INVALID_COMMAND_MESSAGE, STOP_MESSAGE, \
    QUIT_MESSAGE, BASE_COMMANDS, BASE_ERROR_MESSAGE, EMPTY_COMMAND_MESSAGE
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
            input_message = catch_base_errors(app, lambda: handle_commands(app, commands))
        except StopError:
            break
    sys.stderr.write(STOP_MESSAGE)


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


def catch_base_errors(app, function):
    """
    Processes the raised exceptions and returns input message.
    :param app: App(contains the information about the current state of the programme)
    :param function: handler to be executed
    :return: message
    """
    try:
        return function()
    except ValueError as exc:
        sys.stderr.write(str(exc))
        return BASE_ERROR_MESSAGE.format(app.user['name'] if app.user else '')
    except QuitError as exc:
        sys.stderr.write(QUIT_MESSAGE + str(exc))
        return BASE_ERROR_MESSAGE.format(app.user['name'])

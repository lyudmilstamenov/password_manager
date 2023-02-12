from src.models.app import App
from src.common.error_handlers import catch_stop_errors, catch_base_errors
from src.common.erros import ForbiddenOperationError
from src.common.consts import COMMANDS, HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE, INVALID_COMMAND_MESSAGE, \
    BASE_COMMANDS, EMPTY_COMMAND_MESSAGE, ALREADY_LOGGED_IN_ERROR_MESSAGE
from src.interpreters.command_handlers import handle_base_commands, login_or_signup, handle_user_commands


@catch_stop_errors
def run():
    app = App()
    print(HELP_MESSAGE)
    input_message = LOGIN_OR_SIGNUP_MESSAGE
    command = None
    while command != 'STOP':
        commands = extract_commands(input_message)
        input_message = handle_commands(app, commands)


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

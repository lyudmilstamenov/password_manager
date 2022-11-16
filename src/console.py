import user_manager
from app import App
from consts import COMMANDS, HELP_MESSAGE, LOGIN_OR_SIGNUP_MESSAGE
from account_manager import add_account, edit_account, delete_account, view_account


# def __int__(self):
#     self.

def console():
    app = App()

    key = app.client.key('User', 5632499082330112)
    app.user = app.client.get(key)
    print('Please enter "help" in order to get information about the commands.')
    input_message=LOGIN_OR_SIGNUP_MESSAGE
    command = None
    while command != 'STOP':
        input_string = input(input_message)
        input_list = input_string.split()
        commands = [cmd.upper() for cmd in input_list[0:2]] + input_list[2:]
        print(commands)
        command = commands[0]
        if command not in COMMANDS:
            print('Invalid command. '+HELP_MESSAGE)
            continue
        if command == 'HELP':
            visualize_help()
            continue
        if not app.user:
            input_message= login_or_signup(commands, app)
            continue
        handle_user_commands(commands, app)


def login_or_signup(commands, app):
    if commands[0] == 'LOGIN':
        return user_manager.login(app)
    if commands[0] == 'SIGNUP':
        return user_manager.signup(app)
    return 'Please enter "login" or "signup" in order to login/signup or enter "help" in order to get information about the commands.'


def handle_user_commands(commands, app):
    if commands[0] == 'ACCOUNT':
        return handle_account_commands(commands[1:], app)
    if commands[0] == 'ORG':
        handle_org_commands(commands[1:], app)


def handle_account_commands(commands, app):
    if commands[0] == 'ADD':
        return add_account(app)
    if len(commands) < 2:
        raise ValueError('Not enough arguments. '+HELP_MESSAGE)
    if commands[0] == 'EDIT':
        return edit_account(app,commands[1])
    if commands[0] == 'DELETE':
        return delete_account(app,commands[1])
    if commands[0] == 'VIEW':
        return view_account(app,commands[1])



def handle_org_commands(commands, app):
    pass


def visualize_help():
    print('help')


if __name__ == '__main__':
    console()

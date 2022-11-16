import user_manager
from app import App
from consts import COMMANDS
# def __int__(self):
    #     self.

def console():
    app = App()
    print('Please enter "help" in order to get information about the commands.')
    print('Please log in [login] or sign up [signup]: ')
    command = None
    while command != 'STOP':
        input_string = input()
        commands = input_string.split()
        command = commands[0].upper()
        if command not in COMMANDS:
            print('Invalid command. Please enter "help" in order to get information about the commands.')
        if command == 'HELP':
            visualize_help()
            continue
        if app.user:
            login_or_signup(commands)
            continue
        handle_account_commands()





def login_or_signup(commands):
    if command == 'HELP':
        visualize_help()
        continue
    if command == 'LOGIN':
        user_manager.login()
        continue
    if command == 'SIGNUP':
        user_manager.signup()
        continue
    if command != 'STOP':


    # @staticmethod
    # def parse_input(input):
    #     commands = input.split(' ')
    #     if commands[0].


def visualize_help():
    print('help')


if __name__ == '__main__':
    command_parser()

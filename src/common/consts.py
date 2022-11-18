from colorama import Fore

BASE_COMMANDS = ['HELP', 'EXIT', 'STOP', 'CLEAR']
LOGIN_OR_SIGNUP = ['LOGIN', 'SIGNUP', 'LOGOUT']
USER_COMMANDS = ['ACCOUNT', 'ORG', 'CATEGORY']
COMMANDS = BASE_COMMANDS + LOGIN_OR_SIGNUP + USER_COMMANDS
NOT_ENOUGH_ARGUMENTS_MESSAGE = 'The command arguments are not enough or are invalid.'
INVALID_ARGUMENTS_MESSAGE = 'The command arguments are invalid.'
INVALID_COMMAND_MESSAGE = 'The command is invalid. '
HELP_MESSAGE = 'Please enter "help" in order to get information about the commands.'
STOP_MESSAGE = 'The programme stops.'
QUIT_MESSAGE = 'You are quiting the current state of the programme. '
LOGIN_OR_SIGNUP_MESSAGE = 'Please log in [login] or sign up [signup]: '
ENTER_COMMAND_WITH_USER_MESSAGE = '\n' + Fore.GREEN + '{}' + Fore.RESET + ' $ '
SUCCESSFUL_LOGIN_MESSAGE = 'You have successfully logged in. \nHi {}, I am your password manager.\n'
SUCCESSFUL_SIGNUP_MESSAGE = 'You have successfully logged in. Please login into your account.\n$'

WRONG_PWD_MESSAGE = 'Wrong password. You have {} more tries.'
WAIT_MESSAGE = 'You have to wait 30 sec before continuing.'
LOGGED_IN_MESSAGE = '{} $ '

USER_NOT_FOUND_MESSAGE = 'User with username {} was not found.'

USER_EXISTS_MESSAGE = 'User with username {} already exists.'
ONLY_LOGIN_MESSAGE = 'You need to login in order to execute other commands.'

EXCEED_RETRIES_MESSAGE = 'You exceeded the allowed number of wrong entries.'
WEAK_PASSWORD_MESSAGE = Fore.RED + \
                        'The password is weak. Security score: {}' +\
                        Fore.RESET
MODERATE_PASSWORD_MESSAGE = Fore.YELLOW + \
                            'The password is moderate. Security score: {}' +\
                            Fore.RESET
STRONG_PASSWORD_MESSAGE = Fore.GREEN +\
                          'The password is strong. Security score: {}' +\
                          Fore.RESET

KIND_EXISTS_MESSAGE = '{} with the same {} already exists. '
KIND_EXISTS_EXCEEDS_ENTRIES_MESSAGE = KIND_EXISTS_MESSAGE + EXCEED_RETRIES_MESSAGE
CHANGE_PASSWORD_MESSAGE = 'Do you want to change it?[yes/no]'

CLEAR_MESSAGE = 'Please enter "clear" after that in order the password to be removed from the console.'

STRING_PROPERTY_VALIDATION_ERROR_MESSAGE = \
    'Invalid value. The {} can contains only ' \
    'letters, digits and ._-. Enter a valid value or ' \
    'enter "exit" to quit the current state of the programme. '

EMAIL_VALIDATION_ERROR_MESSAGE = 'Invalid email. Enter a valid value or ' \
                                 'enter "exit" to quit the current state of the ' \
                                 'programme. '

URL_VALIDATION_ERROR_MESSAGE = 'Invalid url. Enter a valid value or ' \
                               'enter "exit" to quit the current state of the ' \
                               'programme. '

HELP_INFO = {
    'help': 'This command prints out this information.',
    'stop': 'This command stops the execution of the problem.',
    'clear': 'This command clears the console.',
    'login': 'This command shows the login prompt.',
    'signup': 'This commands shows the signup prompt.',
    'account add': 'This command creates a new account.',
    'account edit <account_name>': 'This command updates the information of the account. When editing a field, '
                                   'set it to "-del" in order to make it empty.',
    'account -rm <account_name>': 'This command deletes the account.',
    'account url <account_name>': 'This command opens the login page of the account if the account has a valid url.',
    'account view -all': 'This command shows the non-sensitive infomation of all accounts who are owned by the '
                         'current user.',
    'account view <account_name>': 'This command shows the non-sensitive infomation of the account.',
    'account copy-pwd <account_name>': 'This command copies the password of the account to your clipboard.',
    'account pwd <account_name>': 'This command shows the password of the account on the console. ' + CLEAR_MESSAGE,
    'category -all <category_name>': 'This command shows the non-sensitive infomation of all accounts who are owned '
                                     'by the current user and are from this category.',
    'category -rm <category_name': 'This command deletes the category and for every account from the category the '
                                   'category property is set to empty.',
    'shortcut info': 'If you use "-last" instead of <account_name> the programme will use the most recently used '
                     'account if this is not the first operation with accounts for the session. '
}

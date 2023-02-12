"""
Contains consts used in all files.
"""
from collections import OrderedDict
from colorama import Fore

BASE_COMMANDS = ['HELP', 'STOP', 'CLEAR', 'LOGOUT', 'GEN']
LOGIN_OR_SIGNUP = ['LOGIN', 'SIGNUP']
USER_COMMANDS = ['ACCOUNT', 'ORG', 'CATEGORY']
COMMANDS = BASE_COMMANDS + LOGIN_OR_SIGNUP + USER_COMMANDS
NOT_ENOUGH_ARGUMENTS_MESSAGE = 'The command arguments are not enough or are invalid.'
INVALID_ARGUMENTS_MESSAGE = 'The command arguments are invalid.'
INVALID_COMMAND_MESSAGE = 'The command is invalid. '
HELP_MESSAGE = 'Please enter "help" in order to get information about the commands.'
STOP_MESSAGE = 'The programme stops.'
GOOGLE_CREDENTIALS_MESSAGE = 'The file with your google credentials was not found. ' \
                             'Check whether the path in anaconda-project.yml is correct. '
QUIT_MESSAGE = 'You are quiting the current state of the programme. '
FORBIDDEN_OPERATION_MESSAGE = 'This operation is not allowed. '
UNKNOWN_ERROR_MESSAGE = 'Unknown error. '
LOGIN_OR_SIGNUP_MESSAGE = 'Please log in [login] or sign up [signup]: '
ENTER_COMMAND_WITH_USER_MESSAGE = '\n' + Fore.GREEN + '{}' + Fore.RESET + ' $ '
SUCCESSFUL_LOGIN_MESSAGE = 'You have successfully logged in. \nHi {},' \
                           ' I am your password manager.' + ENTER_COMMAND_WITH_USER_MESSAGE
SUCCESSFUL_SIGNUP_MESSAGE = 'You have successfully signed up. Please login into your account.\n$ '

ALREADY_LOGGED_IN_ERROR_MESSAGE = 'You are already logged in.'

WRONG_PWD_MESSAGE = 'Wrong password. You have {} more tries.'
WAIT_MESSAGE = 'You have to wait 30 sec before continuing.'

USER_NOT_FOUND_MESSAGE = 'User with username {} was not found.'

USER_EXISTS_MESSAGE = 'User with username {} already exists.'
ONLY_LOGIN_MESSAGE = 'You need to login in order to execute other commands.'

EXCEED_RETRIES_MESSAGE = 'You exceeded the allowed number of wrong entries.'
WEAK_PASSWORD_MESSAGE = Fore.RED + \
                        'The password is weak. Security score: {}' + \
                        Fore.RESET
MODERATE_PASSWORD_MESSAGE = Fore.YELLOW + \
                            'The password is moderate. Security score: {}' + \
                            Fore.RESET
STRONG_PASSWORD_MESSAGE = Fore.GREEN + \
                          'The password is strong. Security score: {}' + \
                          Fore.RESET
BASE_ERROR_MESSAGE = HELP_MESSAGE + ENTER_COMMAND_WITH_USER_MESSAGE

KIND_EXISTS_MESSAGE = '{} with the same {} already exists. '
KIND_EXISTS_EXCEEDS_ENTRIES_MESSAGE = KIND_EXISTS_MESSAGE + EXCEED_RETRIES_MESSAGE
CHANGE_PASSWORD_MESSAGE = 'Do you want to change it?[yes/no]'

CLEAR_MESSAGE = 'Please enter "clear" after that ' \
                'in order the password to be removed from the console.'

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
GENERATE_PWD_MESSAGE = 'Password: {}' + ENTER_COMMAND_WITH_USER_MESSAGE

EMPTY_COMMAND_MESSAGE = 'You need to enter a command.'
INVALID_PWD_LEN_MESSAGE = 'The length of the password must be >=4.'
TOO_LARGE_PWD_LEN_MESSAGE = 'The length of the password must be <=150.'

HELP_INFO_LIST = [
    {'command': 'help', 'info': 'This command prints out this information.'},
    {'command': 'stop', 'info': 'This command stops the execution of the problem.'},
    {'command': 'clear', 'info': 'This command clears the console.'},
    {'command': 'gen [<password_length>]',
     'info': 'This command generates a random password. '
             'If do not set the length of the password, by default it will be 8.\n'
             '<password_length> must be a positive integer.'},
    {'command': 'login',
     'info': 'This command shows the login prompt.'},
    {'command': 'signup',
     'info': 'This commands shows the signup prompt.'},
    {'command': 'account [-o <org_name>] add',
     'info': 'This command creates a new account.'},
    {'command': 'account [-o <org_name>] edit <account_name>',
     'info': 'This command updates the information of the account. When editing a field, '
             'set it to "-del" in order to make it empty.\n'
             'You cannot delete the password with "-del".'},
    {'command': 'account [-o <org_name>] -rm <account_name>',
     'info': 'This command deletes the account.'},
    {'command': 'account [-o <org_name>] url <account_name>',
     'info': 'This command opens the login page of '
             'the account if the account has a valid url.'},
    {'command': 'account [-o <org_name>] view -all',
     'info': 'This command shows the non-sensitive '
             'information of all accounts who are owned by the '
             'current owner(user/org).'},
    {'command': 'account [-o <org_name>] view <account_name>',
     'info': 'This command shows the non-sensitive '
             'information of the account.'},
    {'command': 'account [-o <org_name>] view-by-app <app_name>',
     'info': 'This command shows the non-sensitive '
             'information of all accounts by app name who are owned by the'
             'current owner(user/org).'},
    {'command': 'account [-o <org_name>] copy-pwd <account_name>',
     'info': 'This command copies the password of '
             'the account to your clipboard.'},
    {'command': 'account [-o <org_name>] pwd <account_name>',
     'info': 'This command shows the password of '
             'the account on the console.\n' + CLEAR_MESSAGE},
    {'command': 'account [-o <org_name>] cat <category_name>',
     'info': 'This command shows the non-sensitive '
             'information of all accounts \nwho are owned '
             'by the current user and are from this category.'},
    {'command': 'category [-o <org_name>] -all',
     'info': 'This command shows all categories who are owned '
             'by the current user.'},
    {'command': 'category [-o <org_name>] -rm <category_name',
     'info': 'This command deletes the category '
             'and for every account from the category the '
             'category property is set to empty.'},
    {'command': '"shortcut info"',
     'info': 'If you use "-last" instead of <account_name>/<org_name> the programme will use '
             'the most recently used account/organization \n'
             'if this is not the first operation with account/organization for the session.\n'
             '"-last" for organization can be used only on account commands'
             '(not when modifying the organization)\n'
             ' -o <org_name> allows the user to view, create,update and delete '
             'accounts and categories from an organization.'},
    {'command': 'org all',
     'info': 'This command prints the names of all the organizations you are a member of.'},
    {'command': 'org create [<users>]',
     'info': 'This command creates an organization '
             'with members [<users>](the names of valid users) '
             'and the owner is you.'},
    {'command': 'org delete <org_name>',
     'info': 'This command deletes an organization with name org_name.'},
    {'command': 'org add <org_name> <username>',
     'info': 'This command adds user with username '
             '<username> to the organization <org_name>.'},
    {'command': 'org remove <org_name> <username>',
     'info': 'This command removes user with username '
             '<username> from the organization <org_name>.'},
    {'command': 'org view <org_name>',
     'info': 'This command visualizes the non-sensitive '
             'information of the organization.'},
]
HELP_TABLE_PROPERTIES = {'command': 'Commands',
                         'info': 'Information', }
HELP_TABLE_ORDER = OrderedDict([('command', ''), ('info', '')])

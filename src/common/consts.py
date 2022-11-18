from collections import OrderedDict

from colorama import Fore

BASE_COMMANDS = ['HELP', 'STOP', 'CLEAR', 'LOGOUT']
LOGIN_OR_SIGNUP = ['LOGIN', 'SIGNUP']
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
                        'The password is weak. Security score: {}' + \
                        Fore.RESET
MODERATE_PASSWORD_MESSAGE = Fore.YELLOW + \
                            'The password is moderate. Security score: {}' + \
                            Fore.RESET
STRONG_PASSWORD_MESSAGE = Fore.GREEN + \
                          'The password is strong. Security score: {}' + \
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
    'account view -all': 'This command shows the non-sensitive information of all accounts who are owned by the '
                         'current user.',
    'account view <account_name>': 'This command shows the non-sensitive '
                                   'information of the account.',
    'account copy-pwd <account_name>': 'This command copies the password '
                                       'of the account to your clipboard.',
    'account pwd <account_name>': 'This command shows the password of the account on the console. ' + CLEAR_MESSAGE,
    'category -all <category_name>': 'This command shows the non-sensitive information of all accounts who are owned '
                                     'by the current user and are from this category.',
    'category -rm <category_name': 'This command deletes the category and for every account from the category the '
                                   'category property is set to empty.',
    '"shortcut info"': 'If you use "-last" instead of <account_name> '
                       'the programme will use the most recently used '
                       'account if this is not the first operation with accounts for the session. ',
    'org create [<users>]': 'This command creates an organization with members [<users>](the names of valid users) '
                            'and the owner is you.',
    'org delete <org_name>': 'This command deletes an organization with name org_name.',
    'org add <org_name> <username>': 'This command adds user with username <username> to the organization <org_name>.',
    'org remove <org_name> <username>': 'This command removes user with username '
                                        '<username> from the organization <org_name>.',

}
HELP_INFO_LIST = [{'command': 'help', 'info': 'This command prints out this information.'},
              {'command': 'stop', 'info': 'This command stops the execution of the problem.'},
              {'command': 'clear', 'info': 'This command clears the console.'},
              {'command':
                   'login', 'info': 'This command shows the login prompt.'},
              {'command':
                   'signup', 'info': 'This commands shows the signup prompt.'},
              {'command': 'account add', 'info': 'This command creates a new account.'},
              {'command': 'account edit <account_name>',
               'info': 'This command updates the information of the account. When editing a field, '
                       'set it to "-del" in order to make it empty.'},
              {'command': 'account -rm <account_name>', 'info': 'This command deletes the account.'},
              {'command': 'account url <account_name>',
               'info': 'This command opens the login page of the account if the account has a valid url.'},
              {'command': 'account view -all',
               'info': 'This command shows the non-sensitive information of all accounts who are owned by the '
                       'current user.'},
              {'command': 'account view <account_name>', 'info': 'This command shows the non-sensitive '
                                                                 'information of the account.'},
              {'command': 'account copy-pwd <account_name>', 'info': 'This command copies the password '
                                                                     'of the account to your clipboard.'},
              {'command': 'account pwd <account_name>',
               'info': 'This command shows the password of the account on the console.\n' + CLEAR_MESSAGE},
              {'command': 'category -all <category_name>',
               'info': 'This command shows the non-sensitive information of all accounts who are owned '
                       'by the current user and are from this category.'},
              {'command': 'category -rm <category_name',
               'info': 'This command deletes the category and for every account from the category the '
                       'category property is set to empty.'},
              {'command': '"shortcut info"', 'info': 'If you use "-last" instead of <account_name> '
                                                     'the programme will use the most recently used '
                                                     'account \nif this is not the first operation with accounts for the session. '},
              {'command': 'org create [<users>]',
               'info': 'This command creates an organization with members [<users>](the names of valid users) '
                       'and the owner is you.'},
              {'command': 'org delete <org_name>', 'info': 'This command deletes an organization with name org_name.'},
              {'command': 'org add <org_name> <username>',
               'info': 'This command adds user with username <username> to the organization <org_name>.'},
              {'command': 'org remove <org_name> <username>', 'info': 'This command removes user with username '
                                                                      '<username> from the organization <org_name>.'},
              ]
HELP_TABLE_PROPERTIES = {'command': 'Commands',
                         'info': 'Information', }
HELP_TABLE_ORDER = OrderedDict([('command', ''), ('info', '')])

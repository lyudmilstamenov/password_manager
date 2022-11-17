from collections import OrderedDict

BASE_COMMANDS = ['HELP', 'EXIT', 'STOP', 'CLEAR']
LOGIN_OR_SIGNUP = ['LOGIN', 'SIGNUP', 'LOGOUT']
USER_COMMANDS = ['ACCOUNT', 'ORG', 'CATEGORY']
COMMANDS = BASE_COMMANDS + LOGIN_OR_SIGNUP + USER_COMMANDS
NOT_ENOUGH_ARGUMENTS_MESSAGE = 'The command arguments are not enough or are invalid.'
INVALID_ARGUMENTS_MESSAGE = 'The command arguments are invalid.'
INVALID_COMMAND_MESSAGE = 'The command is invalid. '
HELP_MESSAGE = 'Please enter "help" in order to get information about the commands.'
LOGIN_OR_SIGNUP_MESSAGE = 'Please log in [login] or sign up [signup]: '
ACCOUNT_PROPERTIES = {
    'account_name': 'Account name',
    'app_name': 'App name',
    'login_url': 'Login URL',
    'username': 'Username',
    'email': 'Email',
    'password': 'Password',
    'notes': 'Notes',
    'category': 'Category',
    'owner': 'Owner name'}
ACCOUNTS_ORDER = OrderedDict([('account_name', ''), ('app_name', ''), ('login_url', ''), (
    'username', ''), ('email', ''), ('password', ''), ('notes', ''),
                              ('category', ''), ('owner', '')])

CLEAR_MESSAGE = 'Please enter "clear" after that in order the password to be removed from the console.'

ACCOUNT_EXISTS_MESSAGE = 'Account with account name {} already exists.'

STRING_PROPERTY_VALIDATION_ERROR_MESSAGE = 'Invalid value. The {} can contains only ' \
                                           'letters, digits and ._-. Enter a valid value or ' \
                                           'enter "exit" to quit the current state of the ' \
                                           'programme. '

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

CATEGORY_PROPERTIES = {'category_name': 'Category name', 'accounts': 'Accounts', 'owner': 'Owner name'}
CATEGORIES_ORDER = OrderedDict([('category_name', ''), ('accounts', ''), ('owner', 'Owner name')])

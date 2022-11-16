from collections import OrderedDict

BASE_COMMANDS = ['HELP', 'EXIT', 'STOP', 'CLEAR']
LOGIN_OR_SIGNUP = ['LOGIN', 'SIGNUP']
USER_COMMANDS = ['ACCOUNT', 'ORG', 'CATEGORY']
COMMANDS = BASE_COMMANDS + LOGIN_OR_SIGNUP + USER_COMMANDS
HELP_MESSAGE = 'Please enter "help" in order to get information about the commands.'
LOGIN_OR_SIGNUP_MESSAGE = 'Please log in [login] or sign up [signup]: '
ACCOUNT_PROPERTIES = {'account_name': 'Account name', 'app_name': 'App name', 'login_url': 'Login URL',
                      'username': 'Username', 'email': 'Email', 'password': 'Password', 'notes': 'Notes',
                      'category': 'Category', 'owner': 'Owner name'}
ACCOUNTS_ORDER = OrderedDict([('account_name', 'Account name'), ('app_name', 'App name'), ('login_url', 'Login URL'), (
    'username', 'Username'), ('email', 'Email'), ('password', 'Password'), ('notes', 'Notes'),
                              ('category', 'Category'), ('owner', 'Owner name')])

CLEAR_MESSAGE = 'Please enter "clear" after that in order the password to be removed from the console.'

HELP_INFO = {
    'help': 'This command prints out this information.',
    'stop': 'This command stops the execution of the problem.',
    'clear': 'This command clears the console.',
    'account add': '',
    'account edit <account_name>': 'This command updates the information of the account.',
    'account -rm <account_name>': 'This command deletes the account.',
    'account view -all': 'This command shows the non-sensitive infomation of all accounts who are owned by the '
                         'current user.',
    'account view <account_name>': 'This command shows the non-sensitive infomation of the account.',
    'account copy-pwd <account_name>': 'This command copies the password of the account to your clipboard.',
    'account pwd <account_name>': 'This command shows the password of the account on the console. ' + CLEAR_MESSAGE,
    'category -all <category_name>': 'This command shows the non-sensitive infomation of all accounts who are owned '
                                     'by the current user and are from this category.',
    'category -rm <category_name': 'This command deletes the cattegory and for every account from the category the '
                                   'category property is set to empty.',
    'shortcut info': 'If you use "-last" insted of <account_name> the programme will use the most recently used '
                     'account if this is not the first operation with accounts for the session. '
}

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

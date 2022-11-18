from collections import OrderedDict

from .consts import ENTER_COMMAND_WITH_USER_MESSAGE

SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE = 'Account with {} was successfully created.' \
                                       + ENTER_COMMAND_WITH_USER_MESSAGE
DELETED_ACCOUNT_MESSAGE = 'Account with account name {} was successfully deleted.' \
                          + ENTER_COMMAND_WITH_USER_MESSAGE
UPDATED_ACCOUNT_MESSAGE = 'Account with account name {} was successfully updated.' \
                          + ENTER_COMMAND_WITH_USER_MESSAGE
UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE = 'In order not to change the following property click "enter"'
ACCOUNT_NOT_FOUND_MESSAGE = 'Account with account name {} was not found.'
ACCOUNT_EXISTS_MESSAGE = 'Account with account name {} already exists.'
NO_LAST_ACCOUNT_MESSAGE = 'No account was used recently.'

COPIED_TO_CLIPBOARD_MESSAGE = 'The password was successfully copied to your clipboard.' \
                              + ENTER_COMMAND_WITH_USER_MESSAGE
SHOW_PWD_MESSAGE = 'Your password is {}.' + ENTER_COMMAND_WITH_USER_MESSAGE
INVALID_PASSWORD_MESSAGE = 'Invalid password. The password should contain ' \
                           'at least 6 characters, 1 uppercase letters, ' \
                           '1 digits and 1 special characters. '
URL_OPENED_MESSAGE = 'The login page was successfully opened.' + ENTER_COMMAND_WITH_USER_MESSAGE
URL_NOT_VALID_MESSAGE = 'The login url is invalid.' + ENTER_COMMAND_WITH_USER_MESSAGE

ACCOUNT_NAME_INPUT_MESSAGE = 'account name (This name must be unique per account.): '
APP_NAME_INPUT_MESSAGE = 'app name []: '
LOGIN_URL_INPUT_MESSAGE = 'login url []: '
CATEGORY_INPUT_MESSAGE = 'category []: '
USERNAME_INPUT_MESSAGE = 'username: '
EMAIL_INPUT_MESSAGE = 'email: '
NOTES_INPUT_MESSAGE = 'notes []: '
PWD_INPUT_MESSAGE = 'password: '

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

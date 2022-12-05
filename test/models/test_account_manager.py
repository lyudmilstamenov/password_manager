from app import App
from models.account_manager import add_account


class TestAccountManager:
    def test_add_account(self, mocker):
        mocker.patch('src.models.account_manager.init_account_info', return_value={'account_name': 'account 1'})
        mocker.patch('src.models.account_manager.create_entity', return_value={})
        mocker.patch('src.models.account_manager.save_entity')
        mocker.patch('src.models.account_manager.add_account_to_category')

        app = App()
        app.user = {'name': 'user 1'}
        assert add_account(app, None) == ''
#
#
# def edit_account(app, account_name, owner_entity):
#     account = retrieve_account_by_account_name(app, account_name, owner_entity)
#     print(UPDATE_ACCOUNT_ADDITIONAL_INFO_MESSAGE)
#     account_info = update_account_info(app, account, owner_entity)
#     save_entity(app.client, account, account_info)
#     app.last_account = account
#     return UPDATED_ACCOUNT_MESSAGE.format(account_info['account_name'], app.user['name'])
#
#
# def delete_account(app, account_name, owner_entity):
#     account = retrieve_account_by_account_name(app, account_name, owner_entity)
#     app.client.delete(account.key)
#     app.last_account = None
#     return DELETED_ACCOUNT_MESSAGE.format(account['account_name'], app.user['name'])
#
#
# def view_account(app, command, owner_entity):
#     if command == '-all':
#         return view_all_accounts(app, owner_entity)
#     return view_account_by_account_name(app, command, owner_entity)
#
#
# def view_all_accounts(app, owner_entity):
#     accounts = retrieve_all_accounts_by_user(app.client, owner_entity)
#     visualize_accounts(owner_entity['name'], accounts)
#     app.last_account = None
#     return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
#
#
# def view_account_by_account_name(app, account_name, owner_entity):
#     account = retrieve_account_by_account_name(app, account_name, owner_entity)
#     visualize_accounts(owner_entity['name'], [account])
#     app.last_account = account
#     return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])
#
#
# def visualize_password(app, account_name, owner_entity):
#     """
#     Retrieves the password of the account by account_name and returns it.
#     :param app: App(contains the information about the current state of the programme)
#     :param account_name:
#     :param owner_entity: the owner(User/Organization) of the account
#     :return str:
#     """
#     password = retrieve_account_password(app, account_name, owner_entity)
#     return SHOW_PWD_MESSAGE.format(password, app.user['name'])
#
#
# def copy_password(app, account_name, owner_entity):
#     """
#     Retrieves the password of the account by account_name
#     and copies it to the clipboard.
#     :param app: App(contains the information about the current state of the programme)
#     :param account_name:
#     :param owner_entity: the owner(User/Organization) of the account
#     :return str:
#     """
#     password = retrieve_account_password(app, account_name, owner_entity)
#     pyperclip.copy(password)
#     return COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['name'])
#
#
# def open_url(app, account_name, owner_entity):
#     """
#     Opens the url of the account by account_name.
#     :param app: App(contains the information about the current state of the programme)
#     :param account_name:
#     :param owner_entity: the owner(User/Organization) of the account
# :return str: the appropriate message
# """
# account = retrieve_account_by_account_name(app, account_name, owner_entity)
# url = account['login_url']
# if url and url_validator(url):
#     webbrowser.open(url)
#     return URL_OPENED_MESSAGE.format(app.user['name'])
# return URL_NOT_VALID_MESSAGE.format(app.user['name'])

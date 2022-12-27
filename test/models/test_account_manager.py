import pyperclip

from common.account_consts import SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, SHOW_PWD_MESSAGE, \
    DELETED_ACCOUNT_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE
from src.app import App
from src.models.account_manager import add_account, edit_account, delete_account, visualize_password, copy_password


class TestAccountManager:
    def test_add_account(self, mocker):
        account = type('obj', (object,), {'key': 'value'})()
        owner = type('obj', (object,), {'key': 'owner_val'})()
        mocker.patch('src.models.account_manager.init_account_info', return_value=
        {'account_name': 'account 1', 'category': 'cat1'})
        mocker.patch('src.models.account_manager.create_entity', return_value=account)
        mocker.patch('src.models.account_manager.save_entity')
        mocker.patch('src.models.account_manager.add_account_to_category')

        app = App()
        app.user = {'name': 'user 1'}
        assert add_account(app, owner) == SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE.format('account 1', app.user['name'])

    def test_edit_account(self, mocker):
        owner = type('obj', (object,), {'key': 'owner_val'})()
        mocker.patch('src.models.account_manager.retrieve_account_by_account_name', return_value=
        {'account_name': 'account 1', 'category': 'cat1'})
        mocker.patch('src.models.account_manager.update_account_info', return_value={'account_name': 'account 1'})
        mocker.patch('src.models.account_manager.save_entity')
        mocker.patch('src.models.account_manager.add_account_to_category')

        app = App()
        app.user = {'name': 'user 1'}
        assert edit_account(app, 'account 1', owner) == UPDATED_ACCOUNT_MESSAGE.format('account 1',
                                                                                       app.user['name'])

    def test_delete_account(self, mocker):
        account = type('obj', (object,), {'key': 'account_val'})()
        owner = type('obj', (object,), {'key': 'owner_val'})()
        mocker.patch('src.models.account_manager.retrieve_account_by_account_name', return_value=account)

        app = App()
        app.last_accounts = {'owner_val': {'name': 'acc1'}}
        app.client.delete = lambda x: x
        app.user = {'name': 'user 1'}
        assert delete_account(app, 'account 1', owner) == DELETED_ACCOUNT_MESSAGE.format('account 1',
                                                                                         app.user['name'])

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

    def test_visualize_password(self, mocker):
        mocker.patch('src.models.account_manager.retrieve_account_password', return_value='password')

        app = App()
        app.user = {'name': 'user 1'}
        assert visualize_password(app, 'account 1', None) == SHOW_PWD_MESSAGE.format('password',
                                                                                     app.user['name'])

    def test_copy_password(self, mocker):
        mocker.patch('src.models.account_manager.retrieve_account_password', return_value='password')

        app = App()
        app.user = {'name': 'user 1'}
        assert copy_password(app, 'account 1', None) == COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['name'])
        assert pyperclip.paste() == 'password'



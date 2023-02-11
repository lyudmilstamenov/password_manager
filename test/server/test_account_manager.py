import pyperclip

from src.common.account_consts import SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, SHOW_PWD_MESSAGE, \
    DELETED_ACCOUNT_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE

from src.app import App
from models.managers.account_manager import add_account, edit_account, delete_account, visualize_password, copy_password


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



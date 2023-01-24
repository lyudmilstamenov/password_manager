import pyperclip

from common.org_consts import SUCCESSFULLY_CREATED_ORG_MESSAGE
from models.org_manager import create_organization, add_user_to_organization
from src.common.account_consts import SUCCESSFULLY_CREATED_ACCOUNT_MESSAGE, UPDATED_ACCOUNT_MESSAGE, SHOW_PWD_MESSAGE, \
    DELETED_ACCOUNT_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE

from src.app import App
from src.models.account_manager import add_account, edit_account, delete_account, visualize_password, copy_password


class TestOrgManager:

    def test_create_organization(self, mocker):
        org = type('obj', (object,), {'key': 'value'})()
        owner = type('obj', (object,), {'key': 'owner_val'})()
        # mocker.patch('src.models.org_manager.init_org_info', return_value=
        # {'org_name': 'org 1'})
        mocker.patch('src.models.org_manager.create_entity', return_value=org)
        mocker.patch('src.models.org_manager.save_entity')
        mocker.patch('src.models.org_manager.add_org_to_user')

        app = App()
        app.user = {'name': 'user 1'}
        assert create_organization(app, owner) == SUCCESSFULLY_CREATED_ORG_MESSAGE.format('org 1', app.user['name'])

    def test_add_user_to_organization(self, mocker):
        owner = type('obj', (object,), {'key': 'owner_val'})()
        mocker.patch('src.models.org_manager.retrieve_org', return_value={})
        mocker.patch('src.models.org_manager.check_user_exists', return_value={})

        app = App()
        app.user = {'name': 'user 1'}
        assert add_user_to_organization(app, 'org1', 'user1') == UPDATED_ACCOUNT_MESSAGE.format('account 1',
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

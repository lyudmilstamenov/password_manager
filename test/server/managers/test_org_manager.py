import pyperclip

from src.common.consts import USER_NOT_FOUND_MESSAGE
from test.helper import check_exception_message
from test.helper_classes import Owner, Account, User, Organization
from src.common.org_consts import SUCCESSFULLY_CREATED_ORG_MESSAGE, ADDED_USER_TO_ORG_MESSAGE
from src.common.account_consts import SHOW_PWD_MESSAGE, \
    DELETED_ACCOUNT_MESSAGE, COPIED_TO_CLIPBOARD_MESSAGE

from src.models.app import App
from src.server.managers.org_manager import create_organization, add_user_to_organization
from src.server.managers.account_manager import delete_account, visualize_password, copy_password


class TestOrgManager:

    def test_create_organization(self, mocker):
        org = Organization()
        owner = Owner()
        mocker.patch('src.server.managers.org_manager.init_org_info', return_value=({'name': 'org 1'}, [], []))
        mocker.patch('src.server.managers.org_manager.create_entity', return_value=org)
        mocker.patch('src.server.managers.org_manager.save_entity')
        mocker.patch('src.server.managers.org_manager.add_org_to_user')

        app = App()
        app.user = {'name': 'user 1'}
        assert create_organization(app, owner) == SUCCESSFULLY_CREATED_ORG_MESSAGE.format('org 1', app.user['name'])

    def test_add_user_to_organization__wrong_username(self, mocker):
        mocker.patch('src.server.managers.org_manager.retrieve_org', return_value={})
        mocker.patch('src.server.managers.org_manager.check_user_exists', return_value=[])

        app = App()
        app.user = {'name': 'user 1'}
        check_exception_message(lambda: add_user_to_organization(app, 'org1', 'user1'), ValueError,
                                USER_NOT_FOUND_MESSAGE.format('user1'))

    def test_add_user_to_organization(self, mocker):
        mocker.patch('src.server.managers.org_manager.retrieve_org', return_value={'owner': 'user1', 'users': []})
        mocker.patch('src.server.managers.org_manager.check_user_exists', return_value=[User()])
        mocker.patch('src.server.managers.org_manager.add_org_to_user')
        mocker.patch('src.server.managers.org_manager.save_entity')

        app = App()
        app.user = {'name': 'user 1'}

        assert add_user_to_organization(app, 'org1', 'user1') == \
               ADDED_USER_TO_ORG_MESSAGE.format('user1', 'org1', app.user['name'])

    def test_delete_account(self, mocker):
        account = Account()
        owner = Owner()
        mocker.patch('src.server.managers.account_manager.retrieve_account_by_account_name', return_value=account)

        app = App()
        app.last_accounts = {'owner_val': {'name': 'acc1'}}
        app.client.delete = lambda x: x
        app.user = {'name': 'user 1'}
        assert delete_account(app, 'account 1', owner) == DELETED_ACCOUNT_MESSAGE.format('account 1',
                                                                                         app.user['name'])

    def test_visualize_password(self, mocker):
        mocker.patch('src.server.managers.account_manager.retrieve_account_password', return_value='password')

        app = App()
        app.user = {'name': 'user 1'}
        assert visualize_password(app, 'account 1', None) == SHOW_PWD_MESSAGE.format('password',
                                                                                     app.user['name'])

    def test_copy_password(self, mocker):
        mocker.patch('src.server.managers.account_manager.retrieve_account_password', return_value='password')

        app = App()
        app.user = {'name': 'user 1'}
        assert copy_password(app, 'account 1', None) == COPIED_TO_CLIPBOARD_MESSAGE.format(app.user['name'])
        assert pyperclip.paste() == 'password'

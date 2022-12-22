import pytest

from test.helper import check_exception_message
from src.app import App
from src.models.account_helpers import retrieve_account_by_account_name, retrieve_account_password, \
    update_account_info, populate_account_info


class TestAccountHelpers:

    def test_retrieve_account_by_account_name__without_last_account(self, mocker):
        app = App()
        app.last_account = {}
        owner = type('obj', (object,), {'key': 'value'})()
        mocker.patch('src.models.account_helpers.check_account_exists', return_value=[{'account_name': 'name'}])
        assert retrieve_account_by_account_name(app, 'name', owner) == {
            'account_name': 'name'}

    def test_retrieve_account_by_account_name__with_last_account_with_different_name(self, mocker):
        app = App()
        owner = type('obj', (object,), {'key': 'value'})()
        app.last_account ={1: {'account_name': 'name1'}}
        mocker.patch('src.models.account_helpers.check_account_exists', return_value=[{'account_name': 'name2'}])
        assert retrieve_account_by_account_name(app, 'name2', owner) == {
            'account_name': 'name2'}

    def test_retrieve_account_by_account_name(self, mocker):
        app = App()
        app.last_account = {'1':{'account_name': 'name'}}
        owner = type('obj', (object,), {'key': 'value'})()
        mocker.patch('src.models.account_helpers.check_account_exists')
        assert retrieve_account_by_account_name(app, 'name', owner) == {
            'account_name': 'name'}

    def test_retrieve_account_by_account_name__throws_value_error(self, mocker):
        app = App()
        owner = type('obj', (object,), {'key': 'value'})()
        mocker.patch('src.models.account_helpers.check_account_exists', return_value=None)
        check_exception_message(lambda: retrieve_account_by_account_name(app, 'name', owner), ValueError,
                                'Account with account name name was not found.')

    def test_retrieve_account_password(self, mocker):
        owner = lambda: {'password': 'pwd1'};
        owner.key = 'value'
        mocker.patch('src.models.account_helpers.retrieve_account_by_account_name', return_value={'password': 'pwd2'})
        mocker.patch('src.models.account_helpers.decrypt', return_value='decrypted')
        assert retrieve_account_password(App(), '', owner) == 'decrypted'

    # def test_init_account_info(self, mocker):
    #     owner = type('obj', (object,), {'key': 'key_value'})
    #     owner['password'] = 'password1'
    #     mocker.patch('models.account_helpers.populate_account_info',
    #                  return_value={'account_name': 'name', 'password': 'password2'})
    #     mocker.patch('models.account_helpers.check_account_exists', return_value={'account_name': 'name'})
    #     mocker.patch('models.account_helpers.encrypt', return_value='pwd')
    #     assert init_account_info(App(), owner) == 'decrypted'

    def test_update_account_info(self, mocker):
        mocker.patch('src.models.account_helpers.populate_account_info',
                     return_value={'account_name': '-del', 'password': 'password2', 'category': None})
        mocker.patch('src.models.account_helpers.encrypt', return_value='pwd')
        assert update_account_info(App(), {}, {'password': 'pwd2'}) == {'account_name': '', 'password': 'pwd'}

    def test_populate_account_info(self, mocker):
        inputs = iter(['name', 'app', 'url', 'cat', 'user', 'em@gmail.com', 'notes', 'strong_pwd'])
        mocker.patch('src.models.account_helpers.validate_entity_name', return_value='account name')
        mocker.patch('src.models.account_helpers.validate_string_property', return_value='str')
        mocker.patch('src.models.account_helpers.validate_url', return_value='url')
        mocker.patch('src.models.account_helpers.validate_email', return_value='em@gmail.com')
        mocker.patch('src.models.account_helpers.validate_password', return_value='strong_pwd')
        mocker.patch('src.models.account_helpers.input', return_value=next(inputs))
        mocker.patch('src.models.account_helpers.getpass', return_value=next(inputs))
        assert populate_account_info(App(), None) == {'account_name': 'account name',
                                                      'app_name': 'str',
                                                      'category': 'str',
                                                      'email': 'em@gmail.com',
                                                      'login_url': 'url',
                                                      'notes': 'name',
                                                      'password': 'strong_pwd',
                                                      'pwd_length': 10,
                                                      'username': 'str'}

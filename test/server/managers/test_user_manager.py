from test.helper import check_exception_message
from src.common.consts import SUCCESSFUL_SIGNUP_MESSAGE, SUCCESSFUL_LOGIN_MESSAGE, USER_EXISTS_MESSAGE
from test.helper_classes import User
from src.models.app import App
from src.server.managers.user_manager import signup, login


def mock_input(prompt):
    if prompt == 'username: ':
        return 'test_user'
    if prompt == 'email: ':
        return 'test_user@example.com'
    return 'test_password'


class TestUserManager:

    def test_signup(self, mocker):
        app = App()

        mocker.patch('src.server.managers.user_manager.input', side_effect=mock_input)
        mocker.patch('src.server.managers.user_manager.getpass.getpass', lambda msg: 'test_password12$')
        mocker.patch('src.server.managers.user_manager.check_user_exists', return_value=[])
        mocker.patch('src.server.managers.user_manager.validate_entity_name', return_value='test_user')
        mocker.patch('src.server.managers.user_manager.validate_email', return_value='test_user@example.com')
        mocker.patch('src.server.managers.user_manager.validate_password', return_value='test_password')
        mocker.patch('src.server.managers.user_manager.create_entity', return_value={})
        mocker.patch('src.server.managers.user_manager.save_entity')

        result = signup(app)
        assert result == SUCCESSFUL_SIGNUP_MESSAGE

    def test_signup__with_existing_username(self, mocker):
        app = App()

        mocker.patch('src.server.managers.user_manager.input', side_effect=mock_input)
        mocker.patch('src.server.managers.user_manager.getpass.getpass', lambda msg: 'test_password12$')
        mocker.patch('src.server.managers.user_manager.check_user_exists', return_value=[{'name': 'test_user'}])
        mocker.patch('src.server.managers.user_manager.validate_entity_name', return_value='test_user')
        mocker.patch('src.server.managers.user_manager.validate_email', return_value='test_user@example.com')
        mocker.patch('src.server.managers.user_manager.validate_password', return_value='test_password')
        mocker.patch('src.server.managers.user_manager.create_entity', return_value={})
        mocker.patch('src.server.managers.user_manager.save_entity')

        check_exception_message(lambda: signup(app), ValueError, USER_EXISTS_MESSAGE.format('test_user'))

    def test_login(self, mocker):
        app = App()

        def mock_input(prompt):
            if prompt == 'username: ':
                return 'test_user'
            return 'test_password'

        mocker.patch('src.server.managers.user_manager.check_password', return_value=True)
        mocker.patch('src.server.managers.user_manager.check_user_exists', return_value=[User()])
        mocker.patch('src.server.managers.user_manager.input', side_effect=mock_input)
        mocker.patch('src.server.managers.user_manager.getpass.getpass', lambda msg: 'test_password')
        result = login(app)
        assert result == SUCCESSFUL_LOGIN_MESSAGE.format('test_user', 'test_user')

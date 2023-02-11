import getpass

import pytest

from common.consts import SUCCESSFUL_SIGNUP_MESSAGE, SUCCESSFUL_LOGIN_MESSAGE
from helper_classes import User
from models.app import App
from server.managers.user_manager import signup, login


class TestUserManager:

    def test_signup(self, mocker):
        app = App()

        def mock_input(prompt):
            if prompt == 'username: ':
                return 'test_user'
            if prompt == 'email: ':
                return 'test_user@example.com'
            return 'test_password'

        mocker.patch('src.server.managers.user_manager.input', return_value=mock_input)
        mocker.patch('src.server.managers.user_manager.getpass', lambda: 'test_password')
        result = signup(app)
        assert result == SUCCESSFUL_SIGNUP_MESSAGE

    def test_login(self, mocker):
        app = App()

        def mock_input(prompt):
            if prompt == 'username: ':
                return 'test_user'
            return 'test_password'

        mocker.patch('src.server.managers.user_manager.check_password', return_value=True)
        mocker.patch('src.server.managers.user_manager.check_user_exists', return_value=[User()])
        mocker.patch('src.server.managers.user_manager.input', side_effect=mock_input)
        mocker.patch('src.server.managers.user_manager.getpass', lambda: 'test_password')
        result = login(app)
        assert result == SUCCESSFUL_LOGIN_MESSAGE.format('test_user', 'test_user')

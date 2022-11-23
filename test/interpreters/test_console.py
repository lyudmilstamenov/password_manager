import sys
from io import StringIO

import pytest

from src.app import App
from src.common.consts import EMPTY_COMMAND_MESSAGE, INVALID_COMMAND_MESSAGE, HELP_MESSAGE
from src.interpreters.console import handle_commands


class TestConsole:
    def test_handle_commands__without_commands(self):
        with pytest.raises(ValueError) as exc:
            handle_commands(App(), [])

        assert EMPTY_COMMAND_MESSAGE == str(exc.value)

    def test_handle_commands__with_wrong_command(self):
        capturedOutput = StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        assert '$: ' == handle_commands(App(), ['no_command'])
        sys.stdout = sys.__stdout__  # Reset redirect.
        assert INVALID_COMMAND_MESSAGE + HELP_MESSAGE + '\n' == capturedOutput.getvalue()

    def test_handle_commands__with_login_command(self, mocker):
        mocker.patch('src.interpreters.console.login_or_signup', return_value='logged_in')
        assert 'logged_in' == handle_commands(App(), ['LOGIN'])

    def test_handle_commands__with_base_command(self, mocker):
        mocker.patch('src.interpreters.console.handle_base_commands', return_value='base_command_executed')
        assert 'base_command_executed' == handle_commands(App(), ['CLEAR'])

    def test_handle_commands__with_user_command(self, mocker):
        app = App()
        app.user = {'name': 'user1'}
        mocker.patch('src.interpreters.console.handle_user_commands', return_value='user_command_executed')
        assert 'user_command_executed' == handle_commands(app, ['ACCOUNT', 'VIEW'])

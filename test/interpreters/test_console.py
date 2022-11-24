import sys
from io import StringIO

from helper import check_exception_message
from src.app import App
from src.common.consts import EMPTY_COMMAND_MESSAGE, INVALID_COMMAND_MESSAGE, HELP_MESSAGE
from src.interpreters.console import handle_commands


class TestConsole:
    def test_handle_commands__without_commands(self):
        check_exception_message(lambda: handle_commands(App(), []), ValueError,
                                EMPTY_COMMAND_MESSAGE)

    def test_handle_commands__with_wrong_command(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        assert handle_commands(App(), ['no_command']) == '$: '
        sys.stdout = sys.__stdout__
        assert captured_output.getvalue() == INVALID_COMMAND_MESSAGE + HELP_MESSAGE + '\n'

    def test_handle_commands__with_login_command(self, mocker):
        mocker.patch('src.interpreters.console.login_or_signup', return_value='logged_in')
        assert handle_commands(App(), ['LOGIN']) == 'logged_in'

    def test_handle_commands__with_base_command(self, mocker):
        mocker.patch('src.interpreters.console.handle_base_commands', return_value='base_command_executed')
        assert handle_commands(App(), ['CLEAR']) == 'base_command_executed'

    def test_handle_commands__with_user_command(self, mocker):
        app = App()
        app.user = {'name': 'user1'}
        mocker.patch('src.interpreters.console.handle_user_commands', return_value='user_command_executed')
        assert handle_commands(app, ['ACCOUNT', 'VIEW']) == 'user_command_executed'

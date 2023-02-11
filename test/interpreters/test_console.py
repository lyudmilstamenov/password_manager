from src.models.app import App
from src.common.consts import FORBIDDEN_OPERATION_MESSAGE, ALREADY_LOGGED_IN_ERROR_MESSAGE, \
    EMPTY_COMMAND_MESSAGE, INVALID_COMMAND_MESSAGE, BASE_ERROR_MESSAGE
from src.interpreters.console import handle_commands


class TestConsole:
    def test_handle_commands__without_commands(self, capsys):
        app = App()
        app.user = {'name': 'user1'}
        assert handle_commands(app, []) == BASE_ERROR_MESSAGE.format(app.user['name'])
        captured = capsys.readouterr()
        assert captured.err == EMPTY_COMMAND_MESSAGE

    def test_handle_commands__with_wrong_command(self, capsys):
        app = App()
        app.user = {'name': 'user 1'}
        assert handle_commands(app, ['no_command']) == BASE_ERROR_MESSAGE.format(app.user['name'])
        captured = capsys.readouterr()
        assert captured.err == INVALID_COMMAND_MESSAGE

    def test_handle_commands__with_login_command(self, mocker):
        mocker.patch('src.interpreters.console.login_or_signup', return_value='logged_in')
        assert handle_commands(App(), ['LOGIN']) == 'logged_in'

    def test_handle_commands__with_login_command_when_logged_in(self, mocker, capsys):
        mocker.patch('src.interpreters.console.login_or_signup', return_value='logged_in')
        app = App()
        app.user = {'name': 'user 1'}

        assert handle_commands(app, ['LOGIN']) == BASE_ERROR_MESSAGE.format(app.user['name'])
        captured = capsys.readouterr()
        assert captured.err == FORBIDDEN_OPERATION_MESSAGE + ALREADY_LOGGED_IN_ERROR_MESSAGE

    def test_handle_commands__with_base_command(self, mocker):
        mocker.patch('src.interpreters.console.handle_base_commands', return_value='base_command_executed')
        assert handle_commands(App(), ['CLEAR']) == 'base_command_executed'

    def test_handle_commands__with_user_command(self, mocker):
        app = App()
        app.user = {'name': 'user1'}
        mocker.patch('src.interpreters.console.handle_user_commands', return_value='user_command_executed')
        assert handle_commands(app, ['ACCOUNT', 'VIEW']) == 'user_command_executed'

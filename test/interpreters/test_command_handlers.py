from src.models.app import App
from src.common.consts import NOT_ENOUGH_ARGUMENTS_MESSAGE, INVALID_COMMAND_MESSAGE, INVALID_ARGUMENTS_MESSAGE
from test.helper import check_exception_message
from src.interpreters.command_handlers import handle_user_commands


class TestCommandHandlers:
    def test_handle_user_commands__without_commands(self):
        check_exception_message(lambda: handle_user_commands([], None), ValueError,
                                NOT_ENOUGH_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__with_wrong_commands(self):
        check_exception_message(lambda: handle_user_commands(['wrong', 'commands'], None), ValueError,
                                INVALID_COMMAND_MESSAGE)

    def test_handle_user_commands__with_wrong_account_args(self):
        check_exception_message(lambda: handle_user_commands(['ACCOUNT', 'nothing', 'no', 'no'], App()), ValueError,
                                INVALID_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__with_wrong_org_args(self):
        check_exception_message(lambda: handle_user_commands(['ORG', 'nothing', 'no', 'no'], App()), ValueError,
                                INVALID_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__with_wrong_cat_args(self):
        check_exception_message(lambda: handle_user_commands(['CATEGORY', 'nothing', 'no', 'no'], App()), ValueError,
                                INVALID_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__account_with_not_enough_args(self):
        check_exception_message(lambda: handle_user_commands(['ACCOUNT', 'VIEW'], App()), ValueError,
                                NOT_ENOUGH_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__org_with_not_enough_args(self):
        check_exception_message(lambda: handle_user_commands(['ORG', 'ADD'], App()), ValueError,
                                NOT_ENOUGH_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__cat_with_not_enough_args(self):
        check_exception_message(lambda: handle_user_commands(['CATEGORY', 'ADD'], App()), ValueError,
                                NOT_ENOUGH_ARGUMENTS_MESSAGE)

    def test_handle_user_commands__account(self, mocker):
        mocker.patch('src.interpreters.command_handlers.view_account',
                     return_value='view all executed')
        assert handle_user_commands(['ACCOUNT', 'VIEW', '-all'], App()) == 'view all executed'

    def test_handle_user_commands__org(self,mocker):
        mocker.patch('src.interpreters.command_handlers.view_all_orgs',
                     return_value='view_all_orgs executed')
        assert handle_user_commands(['ORG', 'ALL'], App()) == 'view_all_orgs executed'

    def test_handle_user_commands__cat(self,mocker):
        mocker.patch('src.interpreters.command_handlers.view_all_categories',
                     return_value='view_all_categories executed')

        assert handle_user_commands(['CATEGORY', '-ALL'], App()) == 'view_all_categories executed'

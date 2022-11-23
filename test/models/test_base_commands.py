import sys
import unittest
from unittest import mock

import pytest

import src.models
from src.common.consts import INVALID_PWD_LEN_MESSAGE, INVALID_ARGUMENTS_MESSAGE
from src.app import App
from io import StringIO
import sys
import unittest
from src.models.base_commands import generate_pwd, visualize_help


class TestBaseCommands():
    # @patch('src.models.account_helpers.init_account_info')
    # def test_add_account(self):
    #     account_helpers.init_account_info = mock.Mock(return_value="mocked stuff")
    #     # init_account_info.return_value = 'mocked stuff'
    #     sys.stdout.write("world\nworld\nworld\nworld\nworld\nworld\nworld\nworld\nworld\n")
    #     pytest_conf = Config.fromdictargs({}, ['--capture=no'])
    #
    # app = App()
    # # mocker.patch('src.models.account_helpers.init_account_info', return_value={})
    # # mocker.patch('app.client.key', return_value='')
    # # mocker.patch('datastore.Entity', return_value='')
    # # mocker.patch('populate_account_info')
    # a = add_account(app, None)
    # src.models.account_helpers.init_account_info.assert_called_once_with(app, None)
    # assert a == ''
    # # monkeypatch.setattr('builtins.input', lambda _: "Mark")
    #

    def test_generate_pwd(self):
        app = App()
        pwd = generate_pwd(app, [])
        assert pwd is not None
        assert len(pwd) == 8

    def test_generate_pwd__with_len(self):
        app = App()
        pwd = generate_pwd(app, ['20'])
        assert pwd is not None
        assert len(pwd) == 20

    def test_generate_pwd__with_negative_len(self):
        app = App()
        with pytest.raises(ValueError) as exc:
            generate_pwd(app, ['-2'])
        assert INVALID_PWD_LEN_MESSAGE == str(exc.value)

    def test_generate_pwd__with_invalid_len(self):
        app = App()
        with pytest.raises(ValueError) as exc:
            generate_pwd(app, ['0'])
            assert INVALID_PWD_LEN_MESSAGE == str(exc.value)

    def test_generate_pwd__with_invalid_len_str(self):
        app = App()
        with pytest.raises(ValueError) as exc:
            generate_pwd(app, ['not_digit'])
            INVALID_ARGUMENTS_MESSAGE == str(exc.value)

    def test_help(self):
        capturedOutput = StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        visualize_help()
        sys.stdout = sys.__stdout__  # Reset redirect.
        assert capturedOutput.getvalue() is not None

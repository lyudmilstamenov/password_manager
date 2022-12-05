import sys
import unittest
from unittest import mock

import pytest

import src.models
from helper import check_exception_message
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
        pwd = generate_pwd([])
        assert pwd is not None
        assert len(pwd) == 8

    def test_generate_pwd__with_len(self):
        pwd = generate_pwd(['20'])
        assert pwd is not None
        assert len(pwd) == 20

    def test_generate_pwd__with_negative_len(self):
        check_exception_message(lambda: generate_pwd(['-2']), ValueError,
                                INVALID_PWD_LEN_MESSAGE)

    def test_generate_pwd__with_invalid_len(self):
        check_exception_message(lambda: generate_pwd(['0']), ValueError,
                                INVALID_PWD_LEN_MESSAGE)

    def test_generate_pwd__with_invalid_len_str(self):
        check_exception_message(lambda: generate_pwd(['not_digit']), ValueError,
                                INVALID_ARGUMENTS_MESSAGE)

    def test_help(self):
        captured_output = StringIO()  # Create StringIO object
        sys.stdout = captured_output  # and redirect stdout.
        visualize_help()
        sys.stdout = sys.__stdout__  # Reset redirect.
        assert captured_output.getvalue() is not None

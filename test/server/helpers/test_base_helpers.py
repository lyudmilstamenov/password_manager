import io
import sys
from io import StringIO
from unittest.mock import patch

from test.helper import check_exception_message
from src.common.consts import INVALID_PWD_LEN_MESSAGE, INVALID_ARGUMENTS_MESSAGE
from src.server.helpers.base_helpers import generate_pwd, visualize_help
from test.test_consts import HELPER_EXPECTED_MESSAGE


class TestBaseHelpers:

    def test_visualize_help_with_patch(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            visualize_help()
            expected_output = HELPER_EXPECTED_MESSAGE
            assert fake_stdout.getvalue() == expected_output

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

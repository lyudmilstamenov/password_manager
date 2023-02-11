"""
Contains all decorators for exceptions handling.
"""
import sys

from google.auth.exceptions import DefaultCredentialsError

from .consts import BASE_ERROR_MESSAGE, QUIT_MESSAGE, FORBIDDEN_OPERATION_MESSAGE, \
    GOOGLE_CREDENTIALS_MESSAGE, STOP_MESSAGE, UNKNOWN_ERROR_MESSAGE
from .erros import QuitError, ForbiddenOperationError, StopError


def catch_base_errors(func):
    """
    Processes the raised exceptions and returns input message.
    :param func: handler to be executed
    :return: message
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as exc:
            sys.stderr.write(str(exc))
            return BASE_ERROR_MESSAGE.format(args[0].user['name'] if args[0].user else '')
        except QuitError as exc:
            sys.stderr.write(QUIT_MESSAGE + str(exc))
            return BASE_ERROR_MESSAGE.format(args[0].user['name'])
        except ForbiddenOperationError as exc:
            sys.stderr.write(FORBIDDEN_OPERATION_MESSAGE + str(exc))
            return BASE_ERROR_MESSAGE.format(args[0].user['name'])

    return inner


def catch_stop_errors(func):
    """
    Processes the raised DefaultCredentialsError or StopError exceptions.
    :param func: handler to be executed
    :return:
    """

    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (StopError, KeyboardInterrupt):
            sys.stderr.write(STOP_MESSAGE)
        except DefaultCredentialsError:
            sys.stderr.write(GOOGLE_CREDENTIALS_MESSAGE + STOP_MESSAGE)
        except:  # pylint: disable=bare-except
            sys.stderr.write(UNKNOWN_ERROR_MESSAGE)

    return inner

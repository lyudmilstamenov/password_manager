"""
Helper functions used in many tests.
"""


def check_exception_message(function, exc_type, exc_message):
    """
    Checks whether the function raises an error of type exc_type and with message exc_message
    :param function:
    :param exc_type:
    :param exc_message:
    :return:
    """
    try:
        function()
    except exc_type as exc:
        assert True
        assert str(exc) == exc_message
    else:
        assert False

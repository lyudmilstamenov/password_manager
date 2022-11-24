def check_exception_message(function, exc_type, exc_message):
    try:
        function()
    except exc_type as exc:
        assert True
        assert str(exc) == exc_message
    else:
        assert False

from src.models.account_manager import add_account, populate_account_info


def test_unix_fs(mocker):
    app = None
    # mocker.patch('populate_account_info')
    add_account(app)
    populate_account_info.assert_called_once_with(app)

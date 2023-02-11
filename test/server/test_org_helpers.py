# TODO fix fails

from helper import check_exception_message
from models.app import App
from server.helpers.org_helpers import init_org_info, retrieve_org


class TestOrgsHelpers:
    def test_init_org_info(self, mocker):
        inputs = iter(['name', 'app', 'url', 'cat', 'user', 'em@gmail.com', 'notes', 'strong_pwd'])
        mocker.patch('src.server.helpers.org_helpers.get_hashed_password', return_value='hashed_pwd')
        mocker.patch('src.server.helpers.org_helpers.check_user_exists', return_value=[])
        mocker.patch('src.server.helpers.org_helpers.validate_password', return_value='pwd')
        mocker.patch('src.server.helpers.org_helpers.validate_entity_name', return_value='entity_name')
        mocker.patch('src.server.helpers.account_helpers.input', side_effect=[next(inputs) for i in range(8)])
        assert init_org_info(App(), ['user1', 'user2', 'user3']) == ''

    def test_retrieve_org__without_orgs(self, mocker):
        mocker.patch('src.server.helpers.org_helpers.check_owner_of_org', return_value=[])
        check_exception_message(lambda: retrieve_org(None, None, None), ValueError, '')

    def test_retrieve_org(self, mocker):
        mocker.patch('src.server.helpers.org_helpers.check_owner_of_org', return_value=[{'name': 'name123'}])

        assert retrieve_org(None, None, None) == {'name': 'name123'}

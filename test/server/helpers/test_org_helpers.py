from src.server.helpers.org_helpers import retrieve_org


class TestOrgsHelpers:
    def test_retrieve_org(self, mocker):
        mocker.patch('src.server.helpers.org_helpers.check_owner_of_org', return_value=[{'name': 'name123'}])

        assert retrieve_org(None, None, None) == {'name': 'name123'}

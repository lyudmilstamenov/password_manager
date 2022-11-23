import pytest

from src.app import App
from src.models.org_helpers import retrieve_org, drop_sensitive_info_from_org, init_org_info

# TODO fix fails
# class TestOrgsHelpers:
#     def test_init_org_info(self, mocker):
#         inputs = iter(['name', 'app', 'url', 'cat', 'user', 'em@gmail.com', 'notes', 'strong_pwd'])
#         mocker.patch('src.models.org_helpers.get_hashed_password', return_value='hashed_pwd')
#         mocker.patch('src.models.org_helpers.check_user_exists', return_value=[])
#         mocker.patch('src.models.org_helpers.validate_password', return_value='pwd')
#         mocker.patch('src.models.org_helpers.validate_entity_name', return_value='entity_name')
#         mocker.patch('src.models.account_helpers.input', return_value='name')
#         mocker.patch('src.models.account_helpers.input', return_value= next(inputs))
#         assert init_org_info(App(), ['user1', 'user2', 'user3']) == ''
#
#     def test_retrieve_org__without_orgs(self, mocker):
#         mocker.patch('src.models.org_helpers.check_owner_of_org', return_value=[])
    #
    #     with pytest.raises(ValueError) as exc:
    #         retrieve_org(None, None, None)
    #     assert '' == str(exc.value)
    #
    # def test_retrieve_org(self, mocker):
    #     mocker.patch('src.models.org_helpers.check_owner_of_org', return_value=[{'name': 'name123'}])
    #     assert retrieve_org(None, None, None) == {'name': 'name123'}

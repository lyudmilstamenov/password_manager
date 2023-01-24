from src.app import App
from src.models.category_helpers import drop_sensitive_info_from_category


class TestCategoryHelpers:
    def test_drop_sensitive_info_from_category(self):
        app = App()
        app.client.get = lambda _: {'account_name': 'name'}
        assert drop_sensitive_info_from_category(app, {'accounts': ['key1', 'key2', 'key3']},
                                                 {'name': 'owner_name'}) == {'accounts': ['name', 'name', 'name'],
                                                                             'owner': 'owner_name'}

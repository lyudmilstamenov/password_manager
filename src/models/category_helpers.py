from src.common.category_consts import CATEGORY_NOT_FOUND_MESSAGE
from src.database.base import save_entity
from src.database.datastore_manager import check_category_exists


def remove_all_accounts_from_category(app, category, owner):
    for account_key in category['accounts']:
        remove_account_from_category(app, category['category_name'], account_key, owner)
        account = app.client.get(account_key)
        account['category'] = ''
        app.client.put(account)


def remove_account_from_category(app, category_name, account_key, owner):
    categories = check_category_exists(app.client, category_name, owner)
    if not categories:
        raise ValueError(CATEGORY_NOT_FOUND_MESSAGE.format(category_name))
    category = categories[0]
    category_info = dict(category)
    if account_key in category_info['accounts']:
        category_info['accounts'].remove(account_key)

    save_entity(app.client, category, category_info)


def drop_sensitive_info_from_category(app, category, owner):
    category['owner'] = owner['name']
    accounts_number = len(category['accounts'])
    if accounts_number > 5:
        category['accounts'] = f'{accounts_number} accounts'
        return category
    accounts_names = []
    for account_key in category['accounts']:
        try:
            account = app.client.get(account_key)
            if account:
                accounts_names.append(account['account_name'])
        except AttributeError as exc:
            raise AttributeError('Category has invalid accounts.') from exc
    category['accounts'] = accounts_names
    return category

from google.cloud import datastore

from common.category_consts import CATEGORY_NOT_FOUND_MESSAGE, DELETED_CATEGORY_MESSAGE, \
    REMOVE_CATEGORY_QUESTION_MESSAGE, CATEGORY_NOT_DELETED_MESSAGE
from common.consts import ENTER_COMMAND_WITH_USER_MESSAGE
from common.utils import visualize_accounts, visualize_categories
from database.datastore_manager import retrieve_all_categories_by_user, check_category_exists
from database.base import save_entity


def add_account_to_category(app, category_name, account_key):
    categories = check_category_exists(app.client, category_name, app.user)
    if not categories:
        category_info = {}
        category_info['category_name'] = category_name
        category_info['owner'] = app.user.key
        category_info['accounts'] = [account_key]
        category = datastore.Entity(app.client.key('Category'))
    else:
        category = categories[0]
        category_info = dict(category)
        category_info['accounts'] += [account_key]

    save_entity(app.client, category, category_info)


def remove_account_from_category(app, category_name, account_key):
    categories = check_category_exists(app.client, category_name, app.user)
    if not categories:
        raise ValueError(CATEGORY_NOT_FOUND_MESSAGE.format(category_name))
    category = categories[0]
    category_info = dict(category)
    if account_key in category_info['accounts']:
        category_info['accounts'].remove(account_key)

    save_entity(app.client, category, category_info)


def delete_category(app, category_name):
    categories = check_category_exists(app.client, category_name, app.user)
    if not categories:
        raise ValueError(CATEGORY_NOT_FOUND_MESSAGE.format(category_name))
    category = categories[0]
    if category['accounts']:
        answer = input(REMOVE_CATEGORY_QUESTION_MESSAGE)
        if answer.upper() != 'YES':
            return CATEGORY_NOT_DELETED_MESSAGE.format(app.user['username'])
        remove_all_accounts_from_category(app, category)
    app.client.delete(category.key)
    return DELETED_CATEGORY_MESSAGE.format(category['category_name'], app.user['username'])


def remove_all_accounts_from_category(app, category):
    for account_key in category['accounts']:
        remove_account_from_category(app, category['category_name'], account_key)
        account = app.client.get(account_key)
        account['category'] = ''
        app.client.put(account)


def view_all_accounts_by_category(app, category_name):
    categories = check_category_exists(app.client, category_name, app.user)
    if not categories:
        raise ValueError(f'Category with category name {category_name} was not found.')
    category = categories[0]
    print(f'Category {category_name}: ')
    accounts = []
    for account_key in category['accounts']:
        accounts.append(app.client.get(account_key))
    visualize_accounts(app.user['username'], accounts)


def view_all_categories(app):
    categories = retrieve_all_categories_by_user(app.client, app.user)
    print(categories)
    categories = [drop_sensitive_info_from_category(app, category) for category in categories]
    visualize_categories(categories)
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['username'])


def update_category(app, old_category_name, new_category_name, account_key):
    if new_category_name == old_category_name:
        return
    if old_category_name:
        remove_account_from_category(app, old_category_name, account_key)

    if new_category_name == '-del':
        add_account_to_category(app, '', account_key)
    else:
        add_account_to_category(app, new_category_name, account_key)


def drop_sensitive_info_from_category(app, category):
    category['owner'] = app.user['username']
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

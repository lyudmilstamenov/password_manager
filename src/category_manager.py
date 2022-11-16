from utils import check_category_exists, visualize_accounts, retrieve_all_categories_by_user, visualize_categories
from google.cloud import datastore


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
    category.update(category_info)
    app.client.put(category)


def remove_account_from_category(app, category_name, account_key):
    categories = check_category_exists(app.client, category_name, app.user)
    if not categories:
        raise ValueError(f'Category with category name {category_name} was not found.')
    category = categories[0]
    category_info = dict(category)
    if account_key in category_info['accounts']:
        category_info['accounts'].remove(account_key)
    category.update(category_info)
    app.client.put(category)


def delete_category(app, category_name):
    categories = check_category_exists(app.client, category_name, app.user)
    if not categories:
        raise ValueError(f'Category with category name {category_name} was not found.')
    category = categories[0]
    if category['accounts']:
        answer = input(
            'There are accounts who are part of this category. Are you sure that you want to delete the category?['
            'yes/no]')
        if answer.upper() != 'YES':
            print('The category was not removed.')
            return
        remove_all_accounts_from_category(app, category)
    app.client.delete(category.key)
    print(f'Category with category name {category["category_name"]} was successfully removed.')


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
    visualize_categories(categories,app.user['username'])

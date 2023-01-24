"""
Provides functionalities for modifying categories.
"""

from src.common.category_consts import CATEGORY_NOT_FOUND_MESSAGE, DELETED_CATEGORY_MESSAGE, \
    REMOVE_CATEGORY_QUESTION_MESSAGE, CATEGORY_NOT_DELETED_MESSAGE
from src.common.consts import ENTER_COMMAND_WITH_USER_MESSAGE
from src.common.utils import visualize_accounts, visualize_categories
from src.database.datastore_manager import retrieve_all_categories_by_user, check_category_exists
from src.database.base import save_entity, create_entity
from .category_helpers import remove_all_accounts_from_category, remove_account_from_category, \
    drop_sensitive_info_from_category


def add_account_to_category(app, category_name, account_key, owner_entity):
    """
    Adds an account to the Category entity of the category in the datastore.
    :param app:
    :param category_name:
    :param account_key:
    :param owner_entity:
    :return:
    """
    categories = check_category_exists(app.client, category_name, owner_entity)
    if not categories:
        category_info = {'category_name': category_name,
                         'owner': owner_entity.key, 'accounts': [account_key]}
        category = create_entity(app, 'Category')
    else:
        category = categories[0]
        category_info = dict(category)
        category_info['accounts'] += [account_key]

    save_entity(app.client, category, category_info)


def delete_category(app, category_name, owner_entity):
    """
    Deletes a category by name and owner.
    :param app:
    :param category_name:
    :param owner_entity:
    :return:
    """
    categories = check_category_exists(app.client, category_name, owner_entity)
    if not categories:
        raise ValueError(CATEGORY_NOT_FOUND_MESSAGE.format(category_name))
    category = categories[0]
    if category['accounts']:
        answer = input(REMOVE_CATEGORY_QUESTION_MESSAGE)
        if answer.upper() != 'YES':
            return CATEGORY_NOT_DELETED_MESSAGE.format(app.user['name'])
        remove_all_accounts_from_category(app, category, owner_entity)
    app.client.delete(category.key)
    return DELETED_CATEGORY_MESSAGE.format(category['category_name'], app.user['name'])


def view_all_accounts_by_category(app, category_name, owner_entity):
    """
    Retrieves all accounts by category and owner.
    :param app:
    :param category_name:
    :param owner_entity:
    :return:
    """
    categories = check_category_exists(app.client, category_name, owner_entity)
    if not categories:
        raise ValueError(f'Category with category name {category_name} was not found.')
    category = categories[0]
    print(f'Category {category_name}: ')
    accounts = []
    for account_key in category['accounts']:
        accounts.append(app.client.get(account_key))
    visualize_accounts(app.user['name'], accounts)
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def view_all_categories(app, owner_entity):
    """
    Retrieves all categories by the current user/organization.
    :param app:
    :param owner_entity:
    :return:
    """
    categories = retrieve_all_categories_by_user(app.client, owner_entity)
    categories = [
        drop_sensitive_info_from_category(app, category, owner_entity)
        for category in categories
    ]
    visualize_categories(categories)
    return ENTER_COMMAND_WITH_USER_MESSAGE.format(app.user['name'])


def update_category(app, old_category_name, new_category_name, account_key, owner_entity):
    """
    Deletes the account from the old category and enters it in the new one.
    :param app: App(saves the current state of the programme)
    :param old_category_name:
    :param new_category_name:
    :param account_key: the key of the account which will be transferred
     from one to another category
    :param owner_entity:
    :return:
    """
    if new_category_name == old_category_name:
        return
    if old_category_name:
        remove_account_from_category(app, old_category_name, account_key, owner_entity)

    if new_category_name != '-del':
        add_account_to_category(app, new_category_name, account_key, owner_entity)

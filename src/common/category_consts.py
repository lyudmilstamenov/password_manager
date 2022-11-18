from collections import OrderedDict

from common.consts import ENTER_COMMAND_WITH_USER_MESSAGE

CATEGORY_NOT_FOUND_MESSAGE = 'Category with category name {} was not found.'
DELETED_CATEGORY_MESSAGE = 'Category with category name {} was successfully deleted.' + ENTER_COMMAND_WITH_USER_MESSAGE
REMOVE_CATEGORY_QUESTION_MESSAGE = 'There are accounts who are part of this category. Are you sure that you want to delete the category?[yes/no]'
CATEGORY_NOT_DELETED_MESSAGE = 'The category was not removed.' + ENTER_COMMAND_WITH_USER_MESSAGE

CATEGORY_PROPERTIES = {'category_name': 'Category name', 'accounts': 'Accounts', 'owner': 'Owner name'}
CATEGORIES_ORDER = OrderedDict([('category_name', ''), ('accounts', ''), ('owner', 'Owner name')])
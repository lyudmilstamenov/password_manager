from common.consts import ENTER_COMMAND_WITH_USER_MESSAGE

USERS_NOT_FOUND_MESSAGE = 'The following users {} were not found.'
SUCCESSFULLY_CREATED_ORG_MESSAGE = 'Organization with {} was successfully created.' \
                                   + ENTER_COMMAND_WITH_USER_MESSAGE
DELETED_ORG_MESSAGE = 'Organization with organization name {} was successfully deleted.' \
                      + ENTER_COMMAND_WITH_USER_MESSAGE
ADDED_USER_TO_ORG_MESSAGE = 'User {} was successfully added to organization {}.' \
                            + ENTER_COMMAND_WITH_USER_MESSAGE
REMOVED_USER_FROM_ORG_MESSAGE = 'User {} was successfully removed from organization {}.' \
                                + ENTER_COMMAND_WITH_USER_MESSAGE
REMOVE_YOURSELF_FROM_ORG_MESSAGE = 'You cannot remove yourself from the organization.'
REMOVE_ORG_QUESTION_MESSAGE = 'There are users who are part of this organization. ' \
                              'Are you sure that you want to delete the organization?[yes/no]'
ORG_NOT_DELETED_MESSAGE = 'The organization was not removed.' + ENTER_COMMAND_WITH_USER_MESSAGE

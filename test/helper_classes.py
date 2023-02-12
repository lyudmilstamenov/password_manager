"""
Contains classes used ot mock Datastore entities in the tests.
"""


class Account:
    """
    class used to mock Account entity
    """

    def __init__(self):
        self.key = 'account_val'
        self.account_name = 'account 1'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class Owner:
    """
    class used to mock the entity of the current owner
    """

    def __init__(self):
        self.key = 'owner_val'
        self.owner_name = 'owner 1'
        self.password = 'pwd1'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class Organization:
    """
    class used to mock Organization entity
    """

    def __init__(self):
        self.key = 'org_val'
        self.owner_name = 'org 1'
        self.password = 'pwd1'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class User:
    """
    class used to mock User entity
    """

    def __init__(self):
        self.key = 'user_val'
        self.owner_name = 'user 1'
        self.password = 'pwd1'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

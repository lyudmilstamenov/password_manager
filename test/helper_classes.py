class Account(object):
    def __init__(self):
        self.key = 'account_val'
        self.account_name = 'account 1'

    def __getitem__(self, key):
        return getattr(self, key)



class Owner(object):
    def __init__(self):
        self.key = 'owner_val'
        self.owner_name = 'owner 1'
        self.password = 'pwd1'

    def __getitem__(self, key):
        return getattr(self, key)


class Organization(object):
    def __init__(self):
        self.key = 'org_val'
        self.owner_name = 'org 1'
        self.password = 'pwd1'

    def __getitem__(self, key):
        return getattr(self, key)


class User(object):
    def __init__(self):
        self.key = 'user_val'
        self.owner_name = 'user 1'
        self.password = 'pwd1'

    def __getitem__(self, key):
        return getattr(self, key)
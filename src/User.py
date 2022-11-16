class User:
    def __init__(self, username, email=None):
        self.__username = username
        self.__password = None
        self.__id = None
        self.__email = email

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username
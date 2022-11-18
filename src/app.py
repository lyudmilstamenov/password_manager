import os
from google.cloud import datastore


class App:
    """
    Saves information about the current state of the programme including:
     logged in user, most recently used account and datastore client.
    """

    def __init__(self):
        self.__user = None
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] \
            = 'E:/Hobbies/coding/personal_projects/password_function/credentials.json'

        self.__client = datastore.Client()
        self.__last_account = None

    @property
    def user(self):
        return self.__user

    @property
    def client(self):
        return self.__client

    @property
    def last_account(self):
        return self.__last_account

    @user.setter
    def user(self, user):
        self.__user = user
        self.__last_account = None

    @last_account.setter
    def last_account(self, last_account):
        self.__last_account = last_account

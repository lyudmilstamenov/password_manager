import os
from google.cloud import datastore
class App:
    def __init__(self):
        self.__user = None
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"] = 'E:/Hobbies/coding/personal_projects/password_function/credentials.json'

        self.__client = datastore.Client()

    @property
    def user(self):
        return self.__user

    @property
    def client(self):
        return self.__client

    @user.setter
    def user(self, user):
        self.__user = user




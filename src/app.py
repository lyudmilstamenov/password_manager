"""
App saves the current state of the programme
"""

import os
from google.cloud import datastore


class App:
    """
    Saves information about the current state of the programme including:
     logged in user, most recently used account and datastore client.
    """

    def __init__(self):
        self.__user = None
        # dotenv.load_dotenv()  # exports contents of a `.env` file in the curr dir as environmental variables
        # API_KEY = os.getenv("API_KEY")
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] \
        #     = "../credentials.json"
        print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        self.__client = datastore.Client()
        self.__last_accounts = {}
        self.__last_org = None

    @property
    def user(self):
        """
        Retrieves the current user
        :return: User
        """
        return self.__user

    @property
    def client(self):
        """
        Retrieves the Google Datastore client
        :return:
        """
        return self.__client

    @property
    def last_org(self):
        """
        Retrieves the most recently used organization
        :return: Organization
        """
        return self.__last_org

    @property
    def last_accounts(self):
        """
        Retrieves the most recently used account
        :return: Account
        """
        return self.__last_accounts

    @user.setter
    def user(self, user):
        self.__user = user
        self.__last_accounts = {}
        self.__last_org = None

    @last_org.setter
    def last_org(self, last_org):
        self.__last_org = last_org

    @last_accounts.setter
    def last_accounts(self, last_accounts):
        self.__last_accounts = last_accounts

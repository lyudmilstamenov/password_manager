"""
Contains the wrapper class of the datastore.Client class
"""
from google.cloud.datastore import Client


class DatastoreClient:
    """
    Wrapper class of the datastore.Client class
    """
    def __init__(self):
        self.__client = Client()

    def get(self, key):
        """
        Wrapper of the datastore.Client() get method
        :param key:
        :return:
        """
        return self.__client.get(key)

    def query(self, kind):
        """
        Wrapper of the datastore.Client() query method
        :param kind:
        :return:
        """
        return self.__client.query(kind=kind)

    def put(self, entity):
        """
        Wrapper of the datastore.Client() put method
        :param entity:
        :return:
        """
        self.__client.put(entity)

    def delete(self, key):
        """
        Wrapper of the datastore.Client() delete method
        :param key:
        :return:
        """
        self.__client.delete(key)

    def key(self, kind):
        """
        Wrapper of the datastore.Client() key method
        :param kind:
        :return:
        """
        return self.__client.key(kind)

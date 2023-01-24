"""
Provides basic functionalities for work with the datastore
"""
from google.cloud import datastore


def create_query(client, kind, filters):
    """
    Fetches all entities which pass the filters
    :param client: the Google Datastore client
    :param kind: datastore entity kind
    :param filters: dict with keys and values by which to filter the entities
    :return: list of entities which meet the conditions
    """
    query = client.query(kind=kind)
    for key, value in filters.items():
        query.add_filter(key, '=', value)
    return list(query.fetch())


def save_entity(client, entity, entity_info: dict):
    """
    Saves entity with entity_info to the datastore
    :param client: the Google Datastore client
    :param entity:
    :param entity_info: dict which contains the info of the entity
    :return:
    """
    entity.update(entity_info)
    client.put(entity)


def create_entity(app, kind):
    """
    Creates a new entity in the datastore and returns it.
    :param app:
    :param kind:
    :return:
    """
    return datastore.Entity(app.client.key(kind))

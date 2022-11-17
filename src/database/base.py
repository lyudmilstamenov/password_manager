def create_query(client, kind, filters):
    query = client.query(kind=kind)
    for key, value in filters.items():
        query.add_filter(key, '=', value)
    return list(query.fetch())


def save_entity(client, entity, entity_info):
    entity.update(entity_info)
    client.put(entity)

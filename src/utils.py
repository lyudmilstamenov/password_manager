def check_user_exists(client,username):
    query = client.query(kind='User')
    query.add_filter("username", "=", username)
    return list(query.fetch())
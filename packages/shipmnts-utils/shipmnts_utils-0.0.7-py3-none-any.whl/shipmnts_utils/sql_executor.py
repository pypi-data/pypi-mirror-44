from django.db import connection


def execute_select_query(query, fetch=None):
    data = None
    c = connection.cursor()
    try:
        c.execute(query)
        if fetch and fetch == 'one':
            data = c.fetchone()
        else:
            data = c.fetchall()
    finally:
        c.close()
        return data


def execute_update_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
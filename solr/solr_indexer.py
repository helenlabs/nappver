# DB 읽고, indexing 수행

import sqlite3
import pysolr

db_file = "./../db/test.db"
url = 'http://localhost:8983/solr/solrBoard/'


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None


cur = create_connection(db_file).cursor()
cur.execute("select * from app_info")
rows = cur.fetchall()

solr = pysolr.Solr(url, timeout=10, always_commit=True)

solr.delete(q='*:*')

solr.add([
    {
        'id': ele[0],
        'app_name': ele[1],
        'description': ele[2]
    } for ele in rows
])

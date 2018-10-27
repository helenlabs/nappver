from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import Response
import urllib
import json
import pysolr
import sqlite3
from flask_cors import CORS

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/solrBoard', timeout=10)
db_file = "./../db/test.db"

app = Flask(__name__, static_folder='./htm/static/' )
CORS(app)

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


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/search/', methods=['GET', 'POST'])
def search():
    print(">>>search")

    query=request.args.get('query', 'unknown', type=str)
    print(query)

    solr_results = solr.search("app_name:%s OR description:%s" % (query, query))
    print("Saw {0} solr_results(s).".format(len(solr_results)))

    result_list = []
    conn = create_connection(db_file)
    cur = conn.cursor()
    idx=-1
    for idx, solr_result in enumerate(solr_results):
        print('---------------')
        print(solr_result['id'])
        sql = "select * from app_info where id=?"
        cur.execute(sql, (solr_result['id'],))
        db_row = cur.fetchone()
        print(db_row)
        result_list.append({"order": idx+1, "appId": db_row[0], "appName": db_row[1],
                         "description": db_row[2], "iconUrl": db_row[3]})

    response_hash = {"resultCount":idx+1, "dataList": result_list}
    conn.close()

    jsonString = json.dumps(response_hash, ensure_ascii=False)
    resp = Response(jsonString, status=200, mimetype='application/json')

    print('---------------jsonString-----------------')
    print (jsonString)

    return resp


app.run(host='192.168.110.126', port=9999, debug=True)
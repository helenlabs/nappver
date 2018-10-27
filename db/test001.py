import sqlite3


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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def insert_data(conn, data):
    cur = conn.cursor()
    sql = "insert into app_info(id, name, description, img_url) values (?, ?, ?, ?)"
    cur.execute(sql, data)  # data as a tuple
    conn.commit()


def clear_table(conn):
    cur = conn.cursor()
    sql = "delete from app_info"
    cur.execute(sql)
    conn.commit()


db_file = "./test.db"
sql_create_app_info_table = """ CREATE TABLE IF NOT EXISTS app_info (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        description text,
                                        img_url text
                                    ); """

# SQLite DB 연결
conn = create_connection(db_file)

'''# create table
create_table(conn, sql_create_app_info_table)

# insert data
clear_table(conn)   # 일단 기존 데이터는 날리고 나서..
insert_data(conn, ('com.google.app01', '구글 어플리케이션 001', '이것은 구글 어플리케이션이다.',
                   'http://goo.gl/img/aaa.jpg'))
insert_data(conn, ('io.walnuttree.app01', '월넛트리 자연어처리 어플 짱짱 앱', '월넛트리에서 만든 궁극의 자연어처리 어플리케이션',
                   'http://walnuttree.io/img/bbb.jpg'))
'''
# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# SQL 쿼리 실행
cur.execute("select * from app_info")

# 조건문이 있는 경우는 아래와 같이..
#sql = "select * from customer where category=? and region=?"
#cur.execute(sql, (1, 'SEA'))

# 데이타 Fetch
rows = cur.fetchall()
for idx, row in enumerate(rows):
    print('IDX %d ----------------' % idx)
    print(row)

# Connection 닫기
conn.close()
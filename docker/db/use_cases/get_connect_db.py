import psycopg2

def get_connect_db():
    connection = psycopg2.connect(
        dbname="data-mining-db", user="alessandro", password="15900", host="172.17.0.2"
    )

    cursor = connection.cursor()

    return connection,cursor

def close_db(conn,cur):
    conn.close()
    cur.close()
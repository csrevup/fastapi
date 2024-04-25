import psycopg2
import os

##Connection to DB
connection_string=os.environ.get('testing_db')

def get_query(name):
    ##DB Connection
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        sql="select description from items2 where name = '"+name+"'"
        cur.execute(sql)
        item = cur.fetchone()
        if item==None:
            return "error"
        else:
            return item[0]
    
    except psycopg2.Error as e:
        exit()


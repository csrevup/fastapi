import psycopg2
import os

##Connection to DB
connection_string = "postgresql://postgres:PzDnyALSXLNhGLazCwgxffGjIPNoxHAQ@monorail.proxy.rlwy.net:19847/railway"
connection_2=os.environ.get('DATABASE_URL')

def get_query(name):
    ##DB Connection
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        sql="select description from items2 where name = '"+name+"'"
        cur.execute(sql)
        item = cur.fetchone()
        if item==None:
            return connection_2
        else:
            return item[0]
    
    except psycopg2.Error as e:
        exit()


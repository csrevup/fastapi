import psycopg2

##Connection to DB
connection_string = "postgresql://postgres:PzDnyALSXLNhGLazCwgxffGjIPNoxHAQ@monorail.proxy.rlwy.net:19847/railway"

def get_query(name):
    ##DB Connection
    try:
        conn = psycopg2.connect(connection_string)
        print("Connected to database!")
        cur = conn.cursor()
        sql="select description from items2 where name = " + name
        cur.execute(sql)
        item = cur.fetchone()
        print(item)
    
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        exit()


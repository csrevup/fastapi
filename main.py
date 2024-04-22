from fastapi import FastAPI
import psycopg2

##Connection to DB
connection_string = "postgresql://postgres:PzDnyALSXLNhGLazCwgxffGjIPNoxHAQ@monorail.proxy.rlwy.net:19847/railway"

def db_query (name):
    ##DB Connection
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword, host=dbhost)
        print("Connected to database!")
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        exit()


app = FastAPI()

@app.get("/first_test_api")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}
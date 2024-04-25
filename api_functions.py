import psycopg2
import os

##Connection to DB
connection_string=os.environ.get('testing_db')
connection_string_bonaparte=os.environ.get('bonparte_db')

def get_query(name):
    ##DB Connection
    try:
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                sql = "SELECT description FROM items2 WHERE name = %s"
                cur.execute(sql, (name,))
                item = cur.fetchone()
                return item[0] if item else "No item found."
    except psycopg2.Error as e:
        return f"Database error: {e}"



def piece_sku(piece_name,car_brand,car_model,car_year):
    sql = "select dai FROM vehicle_parts WHERE brand_idf = "+car_brand
    return sql



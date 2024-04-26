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



def piece_sku(piece_name, car_brand, car_model, car_year):
    column_name = "dai"  # Assuming you've confirmed it's always lowercase in your schema
    table_name = "vehicle_parts"
    # Prepare a parameterized query
    query = f'SELECT "{column_name}" FROM {table_name} WHERE line = %s AND brand_idf = %s AND model_idf = %s AND year = %s;'
    
    try:
        with psycopg2.connect(connection_string_bonaparte) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (piece_name, car_brand, car_model, car_year))
                item = cur.fetchone()
                return item[0] if item else "No item found."
    except psycopg2.Error as e:
        return f"Database error: {e}"



import psycopg2
import os
import json

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
    column_names = "dai,application"  # Assuming you've confirmed it's always lowercase in your schema
    table_name = "vehicle_parts"
    # Prepare a parameterized query
    query = f'SELECT DISTINCT {column_names} FROM {table_name} WHERE application ILIKE %s AND brand_idf ILIKE %s AND model_idf ILIKE %s AND year = %s;'
    
    try:
        with psycopg2.connect(connection_string_bonaparte) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (piece_name + '%', car_brand, car_model, car_year))
                items = cur.fetchall()  # Fetch all rows from the query
                if items:
                    return json.dumps([{"sku": item[0], "piece_name": item[1]} for item in items])
                else:
                    return json.dumps({"message": "No items found."})  # Return JSON message if no items are found
    except psycopg2.Error as e:
        return f"Database error: {e}"



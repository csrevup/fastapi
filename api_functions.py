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



def car_part_sku(piece_name, car_brand, car_model, car_year):
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
                     return [{"sku": item[0], "piece_name": item[1]} for item in items]
                else:
                    return {"message": "No items found."}  # Return JSON message if no items are found
    except psycopg2.Error as e:
        return {"error": f"Database error: {e}"}



def sku_details(sku_number):
    column_names_q1 = "dai,application,oem,part_name,position_name"
    column_names_q2 = "brand_idf,model_idf,year"
    table_name = "vehicle_parts"
    # Prepare a parameterized query
    query_q1 = f'SELECT DISTINCT {column_names_q1} FROM {table_name} WHERE dai ILIKE %s;'
    query_q2 = f'SELECT DISTINCT {column_names_q2} FROM {table_name} WHERE dai ILIKE %s;'
    try:
        with psycopg2.connect(connection_string_bonaparte) as conn:
            with conn.cursor() as cur:
                # Execute first query
                cur.execute(query_q1, (sku_number,))
                items = cur.fetchall()
                detailed_items = [{"sku": item[0], "piece_name": item[1], "oem": item[2], "part_name": item[3], "position": item[4]} for item in items] if items else []

                # Execute second query
                cur.execute(query_q2, (sku_number,))
                additional_items = cur.fetchall()
                additional_details = [{"brand": item[0], "model": item[1], "year": str(int(item[2]))} for item in additional_items] if additional_items else []

        # Combine results into a single JSON object
        response = {
            "parts_details": detailed_items,
            "compatible_cars": additional_details
        }
        return response if response['parts_details'] or response['compatible_cars'] else {"message": "No items found."}
    except psycopg2.Error as e:
        return {"error": f"Database error: {e}"}
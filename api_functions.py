import psycopg2
import os
import json

##Connection to DB
connection_string_bonaparte=os.environ.get('bonparte_db')

def car_part_sku_exact(piece_name, car_brand, car_model, car_year):
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
                    result = [{"sku": item[0], "piece_name": item[1]} for item in items]
                    return {"skus": result}
                else:
                    return {"message": "No items found."}  # Return JSON message if no items are found
    except psycopg2.Error as e:
        return {"error": f"Database error: {e}"}

def car_part_sku_similar(piece_name, car_brand, car_model, car_year):
    column_names = "dai, application"
    table_name = "vehicle_parts"

    # Single query fetching all items sorted by similarity
    query = (f"""SELECT DISTINCT {column_names}, similarity(application, '{piece_name}') as smu 
                  FROM {table_name} 
                  WHERE brand_idf ILIKE '{car_brand}' 
                  AND model_idf ILIKE '{car_model}' 
                  AND year = '{car_year}' 
                  ORDER BY similarity(application, '{piece_name}') DESC;""")

    try:
        with psycopg2.connect(connection_string_bonaparte) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

                cur.execute(query)
                items = cur.fetchall()

                # Filter items with similarity of 30% or more
                result = {"accuracy":"high","skus":[{"sku": item[0], "piece_name": item[1], "similarity": item[2]} for item in items if item[2] >= 0.3]}

                if not result["skus"]:
                    # If no items meet the threshold, take the top 2 regardless
                    result = {"accuracy":"low","skus":[{"sku": item[0], "piece_name": item[1], "similarity": item[2]} for item in items if item[2] >= 0.1]}

                if result:
                    return result
                else:
                    return {"accuracy": "No items found"}

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
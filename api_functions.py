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
    column_name = "DAI"
    table_name = "vehicle_parts"
    query = 'select "{0}" from {1} where line= {2} and brand_idf={3} and model_idf={4} and year ={5};'.format(column_name, table_name,piece_name,car_brand,car_model,car_year)
    return query



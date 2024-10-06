import mysql.connector
from utils.constants import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_db_connection():
    try:
        con = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return con
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

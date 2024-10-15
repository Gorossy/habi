import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )
        print("Conexión exitosa a la base de datos")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    return connection

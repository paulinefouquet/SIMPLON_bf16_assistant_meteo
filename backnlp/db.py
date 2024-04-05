import psycopg2
import os


def connect_to_db():
    DB_NAME = os.environ.get("DB_NAME")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("DB_HOST")
    PORT = os.environ.get("PORT")

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        print("Successfully connected to PostgreSQL!")
        cur = conn.cursor()
        return conn, cur

    except Exception as e:
        print(f"Error connecting data into PostgreSQL: {e}")
        return None, None  # Retourne None si la connexion échoue

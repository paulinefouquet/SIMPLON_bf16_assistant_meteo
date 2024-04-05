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


def fetch_perimeter_dep(cur, dep_num):
    cur.execute(
        """
        SELECT DISTINCT latitude, longitude, label
        FROM cities
        WHERE department_number = %s;
    """,
        (dep_num,),
    )
    return cur.fetchall()


def create_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            dt_ref INT,
            dt_forecast TIMESTAMP,
            city_label VARCHAR(100),
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            humidity INT,
            sea_level FLOAT,
            wind_speed FLOAT,
            wind_gust FLOAT,
            wind_direction INT,
            weather_icon VARCHAR(10),
            weather_desc VARCHAR(100),
            CONSTRAINT pk_weather2 PRIMARY KEY (dt_ref, dt_forecast, latitude, longitude)
        );
    """
    )
    print("création de la table")


def insert_data(conn, cur, data, city_data, dt_ref):
    latitude, longitude, label = city_data

    try:
        for item in data:

            dt_forecast = item["dt"]
            temperature = item["T"]["value"]
            humidity = item["humidity"]
            sea_level = item["sea_level"]
            wind_speed = item["wind"]["speed"]
            wind_gust = item["wind"]["gust"]
            wind_direction = item["wind"]["direction"]
            weather_icon = item["weather"]["icon"]
            weather_desc = item["weather"]["desc"]

            try:
                cur.execute(
                    """
                    INSERT INTO weather (dt_ref, dt_forecast, city_label, latitude, longitude, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc)
                    VALUES (%s, TO_TIMESTAMP(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                    (
                        dt_ref,
                        dt_forecast,
                        label,
                        latitude,
                        longitude,
                        temperature,
                        humidity,
                        sea_level,
                        wind_speed,
                        wind_gust,
                        wind_direction,
                        weather_icon,
                        weather_desc,
                    ),
                )
                conn.commit()

            except psycopg2.IntegrityError:
                conn.rollback()
                print("ce jeu de données a déja été chargé.")

    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error inserting data into PostgreSQL: {e}")


def delete_old_data_30h(conn, cur):
    try:
        cur.execute(
            """
            DELETE FROM weather
            WHERE EXTRACT(EPOCH FROM NOW()) - dt_ref > 108000;
        """
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error deleting data older than 10 hours: {e}")
    finally:
        cur.close()

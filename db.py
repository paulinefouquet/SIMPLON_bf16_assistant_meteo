import psycopg2

from config import DB_NAME, USER, PASSWORD, HOST, PORT

def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    print("Successfully connected to PostgreSQL!")
    cur = conn.cursor()
    return conn, cur

def fetch_perimeter_dep(cur, dep_name):
    cur.execute("""
        SELECT DISTINCT latitude, longitude, label
        FROM cities
        WHERE department_name = %s;
    """, (dep_name,))
    return cur.fetchall()

def create_table(cur):
    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather2 (
            dt_ref INT,
            dt_forecast INT,
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
    """)

def insert_data(conn, cur, dt_ref, item, city_data):
    latitude, longitude, label = city_data

    dt_forecast = item['dt']
    temperature = item['T']['value']
    humidity = item['humidity']
    sea_level = item['sea_level']
    wind_speed = item['wind']['speed']
    wind_gust = item['wind']['gust']
    wind_direction = item['wind']['direction']
    weather_icon = item['weather']['icon']
    weather_desc = item['weather']['desc']

    print("insertion des données en cours")
    try:
        cur.execute("""
            INSERT INTO weather2 (dt_ref, dt_forecast, city_label, latitude, longitude, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (dt_ref, dt_forecast, label, latitude, longitude, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc))
        conn.commit()
        print("Données insérées avec succès.")
    except psycopg2.IntegrityError:
        conn.rollback()
        print("Erreur : Cette combinaison de valeurs pour dt_ref, dt_forecast, latitude et longitude existe déjà.")

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
        CREATE TABLE IF NOT EXISTS weather (
            dt_ref INT,
            dt_forecast INT,
            temperature FLOAT,
            humidity INT,
            sea_level FLOAT,
            wind_speed FLOAT,
            wind_gust FLOAT,
            wind_direction INT,
            weather_icon VARCHAR(10),
            weather_desc VARCHAR(100),
            latitude FLOAT,
            longitude FLOAT,
            label VARCHAR(100)
        );
    """)

# def check_data(cur, dt_ref, longitude, latitude, label):
#     # Vérifier si dt_ref existe déjà pour la combinaison de longitude, latitude et label
#     cur.execute("""
#         SELECT COUNT(*) FROM weather
#         WHERE dt_ref = %s AND longitude = %s AND latitude = %s AND label = %s;
#     """, (dt_ref, longitude, latitude, label))

#     # Récupérer le compte
#     count = cur.fetchone()[0]
#     return count

def insert_data(conn, cur, dt_ref, item, city_data):
    longitude, latitude, label = city_data

    # Vérifier si les données existent déjà
    # count = check_data(cur, dt_ref, longitude, latitude, label)

    # if count > 0:
    #     print(f"Les données pour dt_ref {dt_ref} existent déjà pour {label} ({latitude}, {longitude}). L'insertion est ignorée.")
    # else:

    dt_forecast = item['dt']
    temperature = item['T']['value']
    humidity = item['humidity']
    sea_level = item['sea_level']
    wind_speed = item['wind']['speed']
    wind_gust = item['wind']['gust']
    wind_direction = item['wind']['direction']
    weather_icon = item['weather']['icon']
    weather_desc = item['weather']['desc']
        
    cur.execute("""
        INSERT INTO weather (dt_ref, dt_forecast, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc, longitude, latitude, label)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (dt_ref, dt_forecast, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc, longitude, latitude, label))

    # Commit the transaction
    conn.commit()

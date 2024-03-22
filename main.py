import time
import psycopg2

from db import connect_to_db, fetch_perimeter_dep, create_table
from meteo import city_meteo_forecast

DEPARTMENT_PERIMETER = 'gard'

try:
    conn, cur = connect_to_db()
    cities_data = fetch_perimeter_dep(cur, DEPARTMENT_PERIMETER)

    try:
        create_table(cur)

        for city_data in cities_data:
            latitude, longitude, label = city_data
            data = city_meteo_forecast(latitude, longitude)

            # créer un dt_ref unique pour chaque jeu donnée téléchargé
            dt_ref = min(data, key=lambda x: x['dt'])['dt']

            # Insert data into the table
            for item in data:

                dt_forecast = item['dt']
                temperature = item['T']['value']
                humidity = item['humidity']
                sea_level = item['sea_level']
                wind_speed = item['wind']['speed']
                wind_gust = item['wind']['gust']
                wind_direction = item['wind']['direction']
                weather_icon = item['weather']['icon']
                weather_desc = item['weather']['desc']

                try:
                    cur.execute("""
                        INSERT INTO weather2 (dt_ref, dt_forecast, city_label, latitude, longitude, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (dt_ref, dt_forecast, label, latitude, longitude, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc))

                    print("insertion des données en cours")

                    conn.commit()
                except psycopg2.IntegrityError:
                    conn.rollback()
                    print("ce jeu de données a déja été chargé.")

        timestamp_actuel = int(time.time())
        print(f"Data transfer to PostgreSQL succeeded! Dt_load :{timestamp_actuel}")

    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error inserting data into PostgreSQL: {e}")
finally:
    # Close cursor and connection
    cur.close()
    conn.close()
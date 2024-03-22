import time

from db import connect_to_db, fetch_perimeter_dep, create_table
from meteo import city_meteo_forecast

DEPARTMENT_PERIMETER = 'hérault'
timestamp_actuel = int(time.time())

try:
    conn, cur = connect_to_db()
    cities_data = fetch_perimeter_dep(cur, DEPARTMENT_PERIMETER)

    try:
        create_table(cur)

        for city_data in cities_data:
            latitude, longitude, label = city_data
            data = city_meteo_forecast(latitude, longitude)

            # créer une clé de chargement dt_ref qui correspond au min dt des données chargeé

            dt_ref = min(data, key=lambda x: x['dt'])['dt']

            # Vérifier si les données existent déjà

            cur.execute("""
                SELECT COUNT(*) FROM weather
                WHERE dt_ref = %s AND longitude = %s AND latitude = %s AND label = %s;
            """, (dt_ref, latitude, longitude, label))

            count = cur.fetchone()[0]

            if count > 0:
                print(f"Les données pour dt_ref {dt_ref} existent déjà pour {label} ({latitude}, {longitude}). L'insertion est ignorée.")
            
            else:
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
                        
                    cur.execute("""
                        INSERT INTO weather (dt_ref, dt_forecast, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc, longitude, latitude, label)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (dt_ref, dt_forecast, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc, longitude, latitude, label))

                    # Commit the transaction
                    conn.commit()

        print(f"Data transfer to PostgreSQL succeeded! Dt_load :{timestamp_actuel}")

    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error inserting data into PostgreSQL: {e}")
finally:
    # Close cursor and connection
    cur.close()
    conn.close()
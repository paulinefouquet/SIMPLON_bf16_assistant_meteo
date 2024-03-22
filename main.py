import time

from db import connect_to_db, fetch_perimeter_dep, create_table, insert_data
from meteo import city_meteo_forecast

DEPARTMENT_PERIMETER = 'hérault'

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

            insert_data(conn, cur, data, city_data, dt_ref)
        print(f"Data transfer to PostgreSQL succeeded! Dt_load :{dt_ref}")

    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error inserting data into PostgreSQL: {e}")
finally:
    # Close cursor and connection
    cur.close()
    conn.close()
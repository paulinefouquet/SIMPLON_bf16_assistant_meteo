from db import (
    connect_to_db,
    fetch_perimeter_dep,
    create_table,
    insert_data,
    delete_old_data_30h,
)
from meteo import city_meteo_forecast

DEPARTMENT_NUMBER = "09"

conn, cur = connect_to_db()

cities = fetch_perimeter_dep(cur, DEPARTMENT_NUMBER)

create_table(cur)

for city in cities:

    latitude, longitude, label = city
    data_meteo = city_meteo_forecast(latitude, longitude)

    # créer un dt_ref unique pour chaque jeu donnée téléchargé
    dt_ref = min(data_meteo, key=lambda x: x["dt"])["dt"]

    insert_data(conn, cur, data_meteo, city, dt_ref)

print(f"Data transfer to PostgreSQL succeeded! Dt_load :{dt_ref}")

delete_old_data_30h(conn, cur)
print(f"Old data suppressed")

# Close cursor and connection
cur.close()
conn.close()

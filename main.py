from db import (
    connect_to_db,
    fetch_perimeter_dep,
    create_table,
    insert_data,
    delete_old_data_30h,
)
from meteo import city_meteo_forecast

DEPARTMENT_PERIMETER = "hérault"

conn, cur = connect_to_db()

cities_data = fetch_perimeter_dep(cur, DEPARTMENT_PERIMETER)

create_table(cur)

for city_data in cities_data:

    latitude, longitude, label = city_data
    data_meteo = city_meteo_forecast(latitude, longitude)

    # créer un dt_ref unique pour chaque jeu donnée téléchargé
    dt_ref = min(data_meteo, key=lambda x: x["dt"])["dt"]

    insert_data(conn, cur, data_meteo, city_data, dt_ref)

print(f"Data transfer to PostgreSQL succeeded! Dt_load :{dt_ref}")

delete_old_data_30h(conn, cur)
print(f"Old data suppressed")

# Close cursor and connection
cur.close()
conn.close()

from db import (
    connect_to_db,
    fetch_perimeter_dep,
    create_table,
    insert_data,
    delete_old_data_30h,
)
from loading_cities import load_cities
from get_meteo import city_meteo_forecast

from tqdm import tqdm

DEPARTMENT_NUMBER = "34"

conn, cur = connect_to_db()

# Vérifier si la table cities existe
cur.execute(
    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'cities')"
)
table_exists = cur.fetchone()[0]

if not table_exists:
    print("Table 'cities' does not exist. Loading cities data...")
    load_cities()  # Si la table n'existe pas, charger les données des villes

cities = fetch_perimeter_dep(cur, DEPARTMENT_NUMBER)

create_table(cur)

for city in tqdm(cities):

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

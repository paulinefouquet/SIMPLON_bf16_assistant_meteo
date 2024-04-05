import json
from db import connect_to_db


# récupérer les données de la db:
def fetch_city_herault():
    conn, cur = connect_to_db()
    cur.execute(
        """
        SELECT DISTINCT city_label
        FROM weather;
    """
    )
    list_city = cur.fetchall()
    # Fermer la connexion à la base de données
    conn.close()
    # Retourner les données des villes
    city_names = [city[0] for city in list_city]
    return {"cities": city_names}

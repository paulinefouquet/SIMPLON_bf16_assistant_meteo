import requests
import json
import base64

from config import EDENAI_KEY
from db import connect_to_db

# Check if my_key is empty or missing
if not EDENAI_KEY or EDENAI_KEY == "":
    print(
        "Your key is not filled or missing. Please provide a key compatible with EdenAI."
    )

headers = {"Authorization": EDENAI_KEY}


#récupérer les données de la db:
def fetch_forecast_for_city(city, date, hour=None):
    conn, cur = connect_to_db()

    if hour is None:
        timestamp = date
        query = f"""
        SELECT dt_forecast, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_desc
            FROM weather
            WHERE city_label = %s AND date_trunc('day', dt_forecast) = %s
        """
        cur.execute(query, (city, timestamp))
    else:
        timestamp = f"{date} {hour:02}:00:00.000"
        cur.execute(
            f"""
            SELECT dt_forecast, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_desc
                FROM weather
                WHERE city_label = %s AND dt_forecast = %s
            """,
            (city, timestamp),
        )
    columns = [
        "Forecast date and hour",
        "Temperature",
        "Humidity",
        "Sea Level",
        "Wind Speed",
        "Wind Gust",
        "Wind Direction",
        "Weather Description",
    ]
    cities_data = cur.fetchall()
    result = ""
    for row in cities_data:
        result += (
            "\n".join([f"{column} {value}" for column, value in zip(columns, row)])
            + "\n"
        )
    return result.strip()

def generate_text(city: str, date: str, hour=None) -> str:
    meteo_data = fetch_forecast_for_city(city, date, hour=None)

    url = "https://api.edenai.run/v2/text/chat"
    provider = "openai"
    payload = {
        "providers": provider,
        "text": "",
        "chatbot_global_action": f"Act as a fun french weather forecast, remind the {city}, limit your answer to 20 words and do not use any emojis",
        "previous_history": [],
        "temperature": 0.8,
        "max_tokens": 200,
        "fallback_providers": "meta",
    }
    payload["text"] = f"Write a fun weather report about this :{meteo_data}"

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)[provider]
    meteo_text = result["generated_text"]
    return meteo_text

def text_to_speech(meteo_text: str, city: str, date: str, hour=None) -> None:

    url = "https://api.edenai.run/v2/audio/text_to_speech"

    providers = "google"
    language = "fr-FR"
    payload = {
        "providers": providers,
        "language": language,
        "option": "MALE",
        "text": meteo_text,
        "fallback_providers": "",
    }
    
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        
        audio_data = result.get('google', {}).get('audio')
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            if hour is None:
                filename = f"audio_{city}_{date}.mp3"
            else:
                filename = f"audio_{city}_{date}_{hour}.mp3"
            print(f'filename: {filename}')
            with open(f"audio/{filename}", "wb") as audio_file:
                audio_file.write(audio_bytes)
            print(f"Fichier audio généré avec succès : {filename}")
            return filename
        else:
            print("Aucune donnée audio disponible.")
    else:
        print(f"Erreur lors de la requête : {response.status_code} - {response.text}")
from meteofrance_api import MeteoFranceClient

meteo = MeteoFranceClient()


def city_meteo_forecast(lat, long):
    try:
        city_forecast = meteo.get_forecast(lat, long)
        return city_forecast.forecast
    except Exception as e:
        print(f"erreur lors de l'appel à l'API météoFrance: {e}")

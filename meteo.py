from meteofrance_api import MeteoFranceClient

meteo = MeteoFranceClient()

def city_meteo_forecast(lat, long):
    city_forecast = meteo.get_forecast(lat, long)
    return city_forecast.forecast


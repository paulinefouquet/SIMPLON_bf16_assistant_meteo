import pytest
from get_meteo import city_meteo_forecast


def test_city_meteo_forecast_valid_input():

    lat = 48.8566  # Latitude de Paris
    long = 2.3522  # Longitude de Paris

    result = city_meteo_forecast(lat, long)

    # Vérification si le résultat n'est pas vide
    assert result != None
    assert isinstance(result, list)
    assert len(result) == 76
    assert "dt" in result[0]
    assert (result[0]["dt"] % 100) == 0

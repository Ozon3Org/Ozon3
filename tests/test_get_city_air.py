import pandas
import pandas.api.types as pd_types
import pytest

from utils import api


@pytest.mark.vcr
def test_return_value_and_format():
    result = api.get_city_air("london")
    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 1


@pytest.mark.vcr
def test_column_expected_contents():
    result = api.get_city_air("london")
    assert result.at[0, "city"] == "london"  # Exactly like input
    assert result.at[0, "station"] == "London"  # Given by server


@pytest.mark.vcr
def test_column_types():
    result = api.get_city_air("london")
    STR_COLUMNS = [
        "dominant_pollutant",
        "AQI_meaning",
        "AQI_health_implications",
        "timestamp",
        "timestamp_timezone",
    ]
    FLOAT_COLUMNS = [
        "latitude",
        "longitude",
        "aqi",
        "pm2.5",
        "pm10",
        "o3",
        "co",
        "no2",
        "so2",
        "dew",
        "h",
        "p",
        "t",
        "w",
        "wg",
    ]
    assert all([pd_types.is_string_dtype(result[col]) for col in STR_COLUMNS])
    assert all([pd_types.is_float_dtype(result[col]) for col in FLOAT_COLUMNS])


@pytest.mark.vcr
def test_bad_city():
    with pytest.raises(Exception, match="no known AQI station"):
        api.get_city_air("a definitely nonexistent city")

    with pytest.raises(Exception):
        api.get_city_air("")

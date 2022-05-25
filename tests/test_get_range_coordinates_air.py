import numpy
import pandas
import pandas.api.types as pd_types
import pytest

from utils import api

LOWER_BOUND = (51, -0.2)
UPPER_BOUND = (52, 1)


@pytest.mark.vcr
def test_return_value_and_format():
    result = api.get_range_coordinates_air(LOWER_BOUND, UPPER_BOUND)

    # Check return value and format
    assert isinstance(result, pandas.DataFrame)
    assert len(result) > 0  # Should be 32, actually


@pytest.mark.vcr
def test_column_expected_contents():
    result = api.get_range_coordinates_air(LOWER_BOUND, UPPER_BOUND)

    # Sanity check: make sure lat-lon are within range
    assert (result["latitude"] > LOWER_BOUND[0]).all()
    assert (result["latitude"] < UPPER_BOUND[0]).all()
    assert (result["longitude"] > LOWER_BOUND[1]).all()
    assert (result["longitude"] < UPPER_BOUND[1]).all()

    # Range of coordinates: no city was given, hence city must all be nan
    assert numpy.isnan(result["city"]).all()


@pytest.mark.vcr
def test_column_types():
    result = api.get_range_coordinates_air(LOWER_BOUND, UPPER_BOUND)
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
def test_bad_coordinates():
    with pytest.raises(Exception):
        api.get_range_coordinates_air(
            lower_bound=("lol", "bruh"), upper_bound=(0, 0)  # type: ignore
        )

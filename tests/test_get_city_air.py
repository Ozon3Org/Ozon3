import numpy
import pandas
import pandas.api.types as pd_types
import pytest

from utils import api, DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FILE


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
        "pm25",
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
def test_excluded_params():
    # Param should be really excluded when specified as such
    custom_params = ["aqi", "pm25", "o3"]
    result = api.get_city_air("london", params=custom_params)
    assert "pm10" not in result
    assert "pm25" in result


@pytest.mark.vcr
def test_nonexistent_requested_params():
    # Return asked params even when the response does not contain that specific param
    BAD_PARAM_NAME = "param_that_is_not_in_london_aqi"
    result = api.get_city_air("london", params=[BAD_PARAM_NAME])
    param_value = result.at[0, BAD_PARAM_NAME]
    assert numpy.isnan(param_value)


@pytest.mark.vcr
def test_bad_city():
    with pytest.raises(Exception, match="no known AQI station"):
        api.get_city_air("a definitely nonexistent city")

    with pytest.raises(Exception):
        api.get_city_air("")


@pytest.mark.vcr
def test_bad_data_format():
    with pytest.raises(Exception, match="Invalid file format"):
        api.get_city_air("london", data_format="a definitely wrong data format")

    # Calling wrong data format shouldn't create an output folder
    assert not DEFAULT_OUTPUT_FOLDER.exists()


@pytest.mark.vcr
def test_correct_data_format():
    # There shouldn't be an output folder by default
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Not specifying data format shouldn't create an output directory
    api.get_city_air("london")
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Output files should be made
    for fmt in ["xlsx", "csv", "json"]:
        api.get_city_air("london", data_format=fmt)
        assert DEFAULT_OUTPUT_FILE.with_suffix(f".{fmt}").is_file()

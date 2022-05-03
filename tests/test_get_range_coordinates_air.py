import numpy
import pandas
import pandas.api.types as pd_types
import pytest

from utils import (
    api,
    DEFAULT_OUTPUT_FOLDER,
    DEFAULT_OUTPUT_FILE,
    SUPPORTED_OUTPUT_FORMATS,
)

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
def test_excluded_params():
    # Param should be really excluded when specified as such
    custom_params = ["aqi", "pm2.5", "o3"]
    result = api.get_range_coordinates_air(
        LOWER_BOUND, UPPER_BOUND, params=custom_params
    )
    assert "pm10" not in result
    assert "pm2.5" in result


@pytest.mark.vcr
def test_nonexistent_requested_params():
    # Return asked params even when the response does not contain that specific param
    BAD_PARAM_NAME = "param_that_is_not_in_london_aqi"
    result = api.get_range_coordinates_air(
        LOWER_BOUND, UPPER_BOUND, params=[BAD_PARAM_NAME]
    )
    param_value = result.at[0, BAD_PARAM_NAME]
    assert numpy.isnan(param_value)


@pytest.mark.vcr
def test_bad_coordinates():
    with pytest.raises(Exception):
        api.get_range_coordinates_air(lower_bound=("lol", "bruh"), upper_bound=(0, 0))


@pytest.mark.vcr
def test_output_data_format_bad():
    with pytest.raises(Exception, match="Invalid file format"):
        api.get_range_coordinates_air(
            LOWER_BOUND, UPPER_BOUND, data_format="a definitely wrong data format"
        )

    # Calling wrong data format shouldn't create an output folder
    assert not DEFAULT_OUTPUT_FOLDER.exists()


@pytest.mark.vcr
@pytest.mark.parametrize("fmt", SUPPORTED_OUTPUT_FORMATS)
def test_output_data_formats(fmt):

    # Not specifying data format shouldn't create an output directory
    api.get_range_coordinates_air(LOWER_BOUND, UPPER_BOUND)
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Check that output file is made
    api.get_range_coordinates_air(LOWER_BOUND, UPPER_BOUND, data_format=fmt)
    assert DEFAULT_OUTPUT_FILE.with_suffix(f".{fmt}").is_file()

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

COORDS = [(0, 0), (50, 0), (40, -75)]


@pytest.mark.vcr
def test_return_value_and_format():
    result = api.get_multiple_coordinate_air(COORDS)

    # Check return value and format
    assert isinstance(result, pandas.DataFrame)
    assert len(result) == len(COORDS)


@pytest.mark.vcr
def test_column_expected_contents():
    result = api.get_multiple_coordinate_air(COORDS)

    # Coordinate was given, so city should be nan
    assert numpy.isnan(result["city"]).all()


@pytest.mark.vcr
def test_column_types():
    result = api.get_multiple_coordinate_air(COORDS)
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
    result = api.get_multiple_coordinate_air(COORDS, params=custom_params)
    assert "pm10" not in result
    assert "pm2.5" in result


@pytest.mark.vcr
def test_nonexistent_requested_params():
    # Return asked params even when the response does not contain that specific param
    BAD_PARAM_NAME = "bad_param_name"
    result = api.get_multiple_coordinate_air(COORDS, params=[BAD_PARAM_NAME])
    assert numpy.isnan(result[BAD_PARAM_NAME]).all()


@pytest.mark.vcr
def test_bad_coordinates():
    # NOTE, ???
    # See test_get_multiple_city_air, same issue
    BAD_COORDS = [(50, 0), (50, 1), ("lol", "bruh"), ("50.805778", "0.271611")]
    result = api.get_multiple_coordinate_air(BAD_COORDS)

    # Lat-lon columns should remain float even when given bad coords
    assert pd_types.is_float_dtype(result["latitude"])
    assert pd_types.is_float_dtype(result["longitude"])

    # Rows with bad coord should have nan entire row
    assert result.iloc[2, :].isna().all()

    # Rows with float-able string should be float, because
    # WAQI supports such operation on their backend
    assert result.at[3, "latitude"] == 50.805778
    assert result.at[3, "longitude"] == 0.271611


@pytest.mark.vcr
def test_output_data_format_bad():
    with pytest.raises(Exception, match="Invalid file format"):
        api.get_multiple_coordinate_air(
            COORDS, data_format="a definitely wrong data format"
        )

    # Calling wrong data format shouldn't create an output folder
    assert not DEFAULT_OUTPUT_FOLDER.exists()


@pytest.mark.vcr
@pytest.mark.parametrize("fmt", SUPPORTED_OUTPUT_FORMATS)
def test_output_data_formats(fmt):

    # Not specifying data format shouldn't create an output directory
    api.get_multiple_coordinate_air(COORDS)
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Check that output file is made
    api.get_multiple_coordinate_air(COORDS, data_format=fmt)
    assert DEFAULT_OUTPUT_FILE.with_suffix(f".{fmt}").is_file()

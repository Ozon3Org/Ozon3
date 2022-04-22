import numpy
import pandas
import pandas.api.types as pd_types
import pytest

from utils import api, DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FILE


@pytest.mark.vcr
def test_return_value_and_format():
    # London is located on 51.5972 N, 0.1276 W
    result = api.get_coordinate_air(51.51, -0.13)

    # Check return value and format
    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 1


@pytest.mark.vcr
def test_column_expected_contents():
    result = api.get_coordinate_air(51.51, -0.13)

    assert numpy.isnan(result.at[0, "city"])  # No city was given, so nan
    assert result.at[0, "station"] == "London"  # Given by server

    # London's coordinates
    assert result.at[0, "latitude"] == pytest.approx(51.507351)
    assert result.at[0, "longitude"] == pytest.approx(-0.127759)


@pytest.mark.vcr
def test_column_types():
    result = api.get_coordinate_air(51.51, -0.13)
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
    result = api.get_coordinate_air(51.51, -0.13, params=custom_params)
    assert "pm10" not in result
    assert "pm25" in result


@pytest.mark.vcr
def test_nonexistent_requested_params():
    # Return asked params even when the response does not contain that specific param
    BAD_PARAM_NAME = "param_that_is_not_in_london_aqi"
    result = api.get_coordinate_air(51.51, -0.13, params=[BAD_PARAM_NAME])
    param_value = result.at[0, BAD_PARAM_NAME]
    assert numpy.isnan(param_value)


@pytest.mark.vcr
def test_bad_coordinates():
    with pytest.raises(Exception, match="Invalid geo position"):
        api.get_coordinate_air("not a lat", "not a lon")

    with pytest.raises(Exception, match="Invalid geo position"):
        api.get_coordinate_air(None, None)

    with pytest.raises(Exception, match="Invalid geo position"):
        api.get_coordinate_air(numpy.nan, numpy.nan)

    # Giving coordinates as string of numerics is fine,
    # even though it's not in accordance with Ozone's method definition.
    api.get_coordinate_air("51.51", "-0.13")

    # Giving nonsensical coordinates is also fine
    api.get_coordinate_air(5000, 5000)
    api.get_coordinate_air(-5000, -5000)


@pytest.mark.vcr
def test_bad_data_format():
    with pytest.raises(Exception, match="Invalid file format"):
        api.get_coordinate_air(
            51.51, -0.13, data_format="a definitely wrong data format"
        )

    # Calling wrong data format shouldn't create an output folder
    assert not DEFAULT_OUTPUT_FOLDER.exists()


@pytest.mark.vcr
def test_output_formats():
    # Not specifying data format shouldn't create an output directory
    api.get_coordinate_air(51.51, -0.13)
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Check that output file is made
    for fmt in ["xlsx", "csv", "json"]:
        api.get_coordinate_air(51.51, -0.13, data_format=fmt)
        assert DEFAULT_OUTPUT_FILE.with_suffix(f".{fmt}").is_file()

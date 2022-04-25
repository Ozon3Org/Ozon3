import pandas
import pandas.api.types as pd_types
import pytest

from utils import (
    api,
    DEFAULT_OUTPUT_FOLDER,
    DEFAULT_OUTPUT_FILE,
    SUPPORTED_OUTPUT_FORMATS,
)


@pytest.mark.vcr
def test_return_value_and_format():
    # Check return value and format
    result = api.get_city_forecast("london")

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 8


@pytest.mark.vcr
def test_column_types():
    result = api.get_city_forecast("london")

    # The date column contains date information
    assert pd_types.is_datetime64_any_dtype(result["date"])

    # Check that all pollutants and statistics are in column
    # and are of float type
    for param in ["pm25", "pm10", "o3", "uvi"]:
        for stat in ["min", "max", "avg"]:
            assert pd_types.is_float_dtype(result[(param, stat)])


@pytest.mark.vcr
def test_bad_city_input():
    # Check for bad inputs
    with pytest.raises(Exception, match="no known AQI station"):
        api.get_city_forecast("a definitely nonexistent city")

    with pytest.raises(Exception):
        api.get_city_forecast("")


@pytest.mark.vcr
def test_output_data_format_bad_input():
    with pytest.raises(Exception, match="Invalid file format"):
        api.get_city_forecast("london", data_format="a definitely wrong data format")

    # Calling wrong data format shouldn't result in an output folder being made
    assert not DEFAULT_OUTPUT_FOLDER.exists()


@pytest.mark.vcr
@pytest.mark.parametrize("fmt", SUPPORTED_OUTPUT_FORMATS)
def test_output_data_formats(fmt):
    # Not specifying data format shouldn't create an output directory
    api.get_city_forecast("london")
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Output files should be made
    api.get_city_air("london", data_format=fmt)
    assert DEFAULT_OUTPUT_FILE.with_suffix(f".{fmt}").is_file()

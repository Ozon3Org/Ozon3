import pandas
import pandas.api.types as pd_types
import pytest

from utils import api, DEFAULT_OUTPUT_FOLDER


@pytest.mark.vcr
def test_return_value_and_format():
    result = api.get_city_station_options("ukraine")
    assert isinstance(result, pandas.DataFrame)
    assert len(result) > 0  # Shouldn't be empty for 'ukraine'...


@pytest.mark.vcr
def test_columns():
    result = api.get_city_station_options("ukraine")

    # Check all columns exist
    COLUMNS = ["city_id", "country_code", "station_name", "city_url", "score"]
    assert all([col in result for col in COLUMNS])


@pytest.mark.vcr
def test_score_column():
    result = api.get_city_station_options("ukraine")

    # Make sure score is numeric
    assert pd_types.is_numeric_dtype(result["score"])

    # Make sure score is descending
    score = result["score"].tolist()
    assert score == sorted(score, reverse=True)


@pytest.mark.vcr
def test_nonexistent_city():
    # Shouldn't raise Exception, instead ...
    result = api.get_city_station_options("gibberish_nonexistent_place_name")

    # ... should return a dataframe but with length 0 ...
    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 0

    # ... and with all columns just like usual.
    COLUMNS = ["city_id", "country_code", "station_name", "city_url", "score"]
    assert all([col in result for col in COLUMNS])


@pytest.mark.vcr
def test_no_output_directory():
    api.get_city_station_options("ukraine")

    # There shouldn't be an output folder after calling this method
    assert not DEFAULT_OUTPUT_FOLDER.exists()

import pandas
import pandas.api.types as pd_types
import pytest

from utils import api


# Filterwarnings from: https://stackoverflow.com/a/58645998/11316205
@pytest.mark.vcr
@pytest.mark.slow
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_return_value_and_format():
    result = api.get_historical_data(city="london")
    assert isinstance(result, pandas.DataFrame)


@pytest.mark.vcr
@pytest.mark.slow
def test_column_types():
    result = api.get_historical_data(city_id=5724)

    # The date column contains date information
    assert pd_types.is_datetime64_any_dtype(result["date"])

    HISTORICAL_COLUMNS = ["pm2.5", "pm10", "o3", "no2", "so2", "co"]
    assert all([pd_types.is_float_dtype(result[col]) for col in HISTORICAL_COLUMNS])


@pytest.mark.vcr
@pytest.mark.slow
def test_warnings_on_input_combo():
    with pytest.warns(UserWarning, match="city_id was not supplied"):
        api.get_historical_data(city="london")

    # There should be no warning if supplying city_id only
    api.get_historical_data(city_id=5724)

    # Warn user when both city and city_id are supplied
    with pytest.warns(UserWarning, match="will be ignored"):
        api.get_historical_data(city="london", city_id=5724)


def test_arguments_not_named():
    with pytest.raises(ValueError, match="must be specified"):
        api.get_historical_data("london")  # type: ignore

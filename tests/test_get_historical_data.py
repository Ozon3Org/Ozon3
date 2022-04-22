import pandas
import pytest

from utils import api, DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FILE


@pytest.mark.vcr
@pytest.mark.filterwarnings(
    "ignore::UserWarning"
)  # https://stackoverflow.com/a/58645998/11316205
def test_return_value_and_format():
    result = api.get_historical_data(city="london")
    assert isinstance(result, pandas.DataFrame)


@pytest.mark.vcr
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
        api.get_historical_data("london")


@pytest.mark.vcr
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_correct_data_format():
    # Not specifying data format shouldn't create an output directory
    api.get_historical_data(city_id=5724)
    assert not DEFAULT_OUTPUT_FOLDER.exists()

    # Check that output file is made
    for fmt in ["xlsx", "csv", "json"]:
        api.get_historical_data(city="london", data_format=fmt)
        assert DEFAULT_OUTPUT_FILE.with_suffix(f".{fmt}").is_file()

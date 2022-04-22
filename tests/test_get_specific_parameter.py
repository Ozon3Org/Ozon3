import numpy
import pytest

from utils import api


@pytest.mark.vcr
def test_return_value():
    result = api.get_specific_parameter("london", "aqi")

    assert isinstance(result, float)


@pytest.mark.vcr
def test_nonexistent_requested_param():
    # NOTE, QUESTION (lahdjirayhan)
    # Should nonexistent param return nan or raise Exception? (see code)
    BAD_PARAM_NAME = "bad_param_name"
    result = api.get_specific_parameter("london", BAD_PARAM_NAME)
    assert numpy.isnan(result)


@pytest.mark.vcr
def test_bad_city():
    with pytest.raises(Exception, match="no known AQI station"):
        api.get_specific_parameter("a definitely nonexistent city", "aqi")

    with pytest.raises(Exception):
        api.get_specific_parameter("", "aqi")

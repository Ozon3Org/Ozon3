import pytest

from utils import api


@pytest.mark.vcr
def test_return_value():
    result = api.get_specific_parameter("london", "aqi")

    assert isinstance(result, float)


@pytest.mark.vcr
def test_bad_city():
    with pytest.raises(Exception, match="no known AQI station"):
        api.get_specific_parameter("a definitely nonexistent city", "aqi")

    with pytest.raises(Exception):
        api.get_specific_parameter("", "aqi")

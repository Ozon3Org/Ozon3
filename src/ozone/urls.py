from dataclasses import dataclass


# This prevents the data attributes in the class from being modified.
# This is to ensure that a user/method doesn't accidentally modify the
# endpoint urls stored here.
@dataclass(frozen=True)
class URLs:

    # Base API endpoint.
    _base_url: str = "https://api.waqi.info/"

    # For air quality data search by location.
    search_aqi_url: str = f"{_base_url}feed/"

    # For search for air quality measuring stations in area.
    find_stations_url: str = f"{_base_url}search/"


if __name__ == "__main__":
    pass

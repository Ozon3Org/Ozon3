"""urls module for the Ozone package.

This module contains the URLs dataclass for the package.

It should only be used with the Ozone package and not run directly.
"""

from dataclasses import dataclass


# This prevents the data attributes in the class from being modified.
# This is to ensure that a user/method doesn't accidentally modify the
# endpoint urls stored here.
@dataclass(frozen=True)
class URLs:
    """Class that contains the endpoint urls for the WAQI API

    This class should not be instantiated. It only contains class level attributes,
    and no methods at all. It is a static dataclass.

    Attributes:
        search_aqi_url (str): The endpoint used for retrieving air quality data.
        find_stations_url (str): The endpoint used for
         retrieving a collection of air quality measuring stations.
        find_coordinates_url (str): The endpoint used for
         retrieving geographical information
    """

    # Base API endpoint.
    _base_url: str = "https://api.waqi.info/"

    # For air quality data search by location.
    search_aqi_url: str = f"{_base_url}feed/"

    # For search for air quality measuring stations in area.
    find_stations_url: str = f"{_base_url}search/"

    # For Map Queries
    find_coordinates_url: str = f"{_base_url}map/"


if __name__ == "__main__":
    pass

import pandas
import numpy
import requests
import json
from .urls import URLs

from typing import Any, Dict, List, Union


class Ozone:
    _search_aqi_url: str = URLs.search_aqi_url
    _find_stations_url: str = URLs.find_stations_url
    _default_params: List[str] = [
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

    def __init__(self, token: str = ""):
        self.token: str = token
        self._check_token_validity()

    def _check_token_validity(self) -> None:
        """Check if the token is valid
        """
        test_city: str = "london"
        r = self._make_api_request(
            f"{self._search_aqi_url}/{test_city}/?token={self.token}"
        )

        if self._check_status_code(r):
            if json.loads(r.content)["status"] != "ok":
                print("Warning: Token may be invalid!")

    def _make_api_request(self, url: str) -> requests.Response:
        """Make an API request

        Args:
            url (str): The url to make the request to.

        Returns:
            requests.Response: The response from the API.
        """
        r = requests.get(url)
        return r

    def _check_status_code(self, r: requests.Response) -> bool:
        """Check the status code of the response"""
        if r.status_code == 200:
            return True
        elif r.status_code == 401:
            raise Exception("Unauthorized!")
        elif r.status_code == 404:
            raise Exception("Not Found!")
        elif r.status_code == 500:
            raise Exception("Internal Server Error!")
        return False

    def reset_token(self, token: str) -> None:
        """Use this method to set your API token

        Args:
            token (str): The new API token.
        """
        self.token = token
        self._check_token_validity()

    def get_city_air(
        self,
        city: str,
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get a city's air quality data

        Args:
            city (str): The city to get data for.
            df (pandas.DataFrame, optional): An existing dataframe to append the data to.
            params (List[str], optional): A list of parameters to get data for.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
        """
        if params == [""]:
            params = self._default_params

        r = self._make_api_request(f"{self._search_aqi_url}/{city}/?token={self.token}")
        if self._check_status_code(r):
            # Get all the data.
            data_obj = json.loads(r.content)["data"]
            row = self._parse_data(data_obj, city, params)

            df = pandas.concat([df, pandas.DataFrame(row)], ignore_index=True)
        return df

    def _parse_data(
        self, data_obj: Any, city: str, params: List[str]
    ) -> List[Dict[str, Union[str, float]]]:
        """Parse the data from the API response

        Args:
            data_obj (dict): The data from the API response.

        Returns:
            list: A list of dictionaries containing the data.
        """
        # A single row of data for the dataframe.
        row: Dict[str, Union[str, float]] = {}

        row["city"] = f"{city}"
        row["latitude"] = data_obj["city"]["geo"][0]
        row["longitude"] = data_obj["city"]["geo"][1]
        row["station"] = data_obj["city"]["name"]
        row["dominant_pollutant"] = data_obj["dominentpol"]
        row["timestamp"] = data_obj["time"]["s"]
        row["timestamp_timezone"] = data_obj["time"]["tz"]

        for param in params:
            try:
                if param == "aqi":
                    # This is in different part of JSON object.
                    row["aqi"] = float(data_obj["aqi"])
                else:
                    row[param] = float(data_obj["iaqi"][param]["v"])
            except KeyError:
                # Gets triggered if the parameter is not provided by station.
                row[param] = numpy.nan
        return [row]

    def get_multiple_city_air(
        self,
        cities: List[str],
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get multiple cities' air quality data

        Args:
            cities (list): A list of cities to get data for.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
        """
        for city in cities:
            df = self.get_city_air(city, df, params)
        return df


if __name__ == "__main__":
    pass

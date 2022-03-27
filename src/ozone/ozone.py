"""Ozone module for the Ozone package.

This module contains the main Ozone class, which is used for all live-data
collection done by the Ozone package.

This module should be used only as a part of the Ozone package, and should not
be run directly.

Attributes (module level):
    CALLS (int=1000): The number of calls per second allowed by the WAQI API is 1000.
    RATE_LIMIT (int=1): The time period in seconds for the max number of calls is
        1 second.
"""

import pandas
import numpy
import requests
import json
import itertools
from pathlib import Path
import warnings
from ratelimit import limits, sleep_and_retry
from .urls import URLs

from typing import Any, Dict, List, Union, Tuple

# 1000 calls per second is the limit allowed by API
CALLS: int = 1000
RATE_LIMIT: int = 1


class Ozone:
    """Primary class for Ozone API

    This class contains all the methods used for live data collection.
    This class should be instantiated, and methods should be called from the
    instance.

    Attributes:
        token (str): The private API token for the WAQI API service.
        output_dir_path (str): The path to the directory where
        any output artifacts will be created
    """

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

    def __init__(self, token: str = "", output_path: str = "."):
        """Initialises the class instance and sets the API token value

        Args:
            token (str): The users private API token for the WAQI API.
            output_path (str): The path to the location where
            any output artifacts will be created
        """
        self.token: str = token
        self._check_token_validity()

        self.output_dir_path: Path = Path(output_path, "ozone_output")
        self.output_dir_path.mkdir(exist_ok=True)

    def _check_token_validity(self) -> None:
        """Check if the token is valid"""
        test_city: str = "london"
        r = self._make_api_request(
            f"{self._search_aqi_url}/{test_city}/?token={self.token}"
        )

        self._check_status_code(r)
        if json.loads(r.content)["status"] != "ok":
            warnings.warn("Token may be invalid!")

    @sleep_and_retry
    @limits(calls=CALLS, period=RATE_LIMIT)
    def _make_api_request(self, url: str) -> requests.Response:
        """Make an API request

        Args:
            url (str): The url to make the request to.

        Returns:
            requests.Response: The response from the API.
        """
        r = requests.get(url)
        return r

    def _check_status_code(self, r: requests.Response) -> None:
        """Check the status code of the response"""
        if r.status_code == 200:
            pass
        elif r.status_code == 401:
            raise Exception("Unauthorized!")
        elif r.status_code == 404:
            raise Exception("Not Found!")
        elif r.status_code == 500:
            raise Exception("Internal Server Error!")
        else:
            raise Exception(f"Error! Code {r.status_code}")

    def reset_token(self, token: str) -> None:
        """Use this method to set your API token

        Args:
            token (str): The new API token.
        """
        self.token = token
        self._check_token_validity()

    def _format_output(
        self,
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
    ) -> pandas.DataFrame:
        """Format output data

        Args:
            data_format (str): File format. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            df (pandas.DataFrame,): Dataframe object of air quality data.

        Returns:
            pandas.DataFrame: The dataframe containing the air quality data.
            None: print the string response of file type created.
        """
        if data_format == "df":
            return df
        elif data_format == "csv":
            df.to_csv(Path(self.output_dir_path, "air_quality.csv"), index=False)
            print(f"File saved to disk at {self.output_dir_path} as air_quality.csv")
        elif data_format == "json":
            df.to_json(Path(self.output_dir_path, "air_quality_data.json"))
            print(
                f"File saved to disk at {self.output_dir_path} as air_quality_data.json"
            )
        elif data_format == "xlsx":
            df.to_excel(
                Path(self.output_dir_path, "air_quality_data.xlsx"),
            )
            print(
                f"File saved to disk at {self.output_dir_path} as air_quality_data.xlsx"
            )
        else:
            raise Exception(
                f"Invalid file format {data_format}. Use any of: csv, json, xlsx, df"
            )
        return pandas.DataFrame()

    def _parse_data(
        self, data_obj: Any, city: str, params: List[str] = [""]
    ) -> Dict[str, Union[str, float]]:
        """Parse the data from the API response

        Args:
            data_obj (JSON object returned by json.loads): The data from the API's
                response.
            city (str): The city name.
            params (List[str]): The parameters to parse.

        Returns:
            list: A list containing a single dictionary with the data.
        """
        if params == [""]:
            params = self._default_params

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
                    # This adds AQI_meaning and AQI_health_implications data
                    (
                        row["AQI_meaning"],
                        row["AQI_health_implications"],
                    ) = self._AQI_meaning(float(data_obj["aqi"]))
                else:
                    row[param] = float(data_obj["iaqi"][param]["v"])
            except KeyError:
                # Gets triggered if the parameter is not provided by station.
                row[param] = numpy.nan

        return row

    def _AQI_meaning(self, aqi: float) -> Tuple[str, str]:
        """Retrieve AQI meaning and health implications

        Args:
            row["aqi"] (float): parsed AQI data.

        Returns:
            str: The meaning and health implication of the AQI data.
        """

        if 0 <= aqi <= 50:
            AQI_meaning = "Good"
            AQI_health_implications = (
                "Air quality is considered satisfactory, "
                "and air pollution poses little or no risk"
            )
        elif 51 <= aqi <= 100:
            AQI_meaning = "Moderate"
            AQI_health_implications = (
                "Air quality is acceptable; however, for some pollutants "
                "there may be a moderate health concern for a very small "
                "number of people who are unusually sensitive to air pollution."
            )
        elif 101 <= aqi <= 150:
            AQI_meaning = "Unhealthy for sensitive group"
            AQI_health_implications = (
                "Members of sensitive groups may experience health effects. "
                "The general public is not likely to be affected."
            )
        elif 151 <= aqi <= 200:
            AQI_meaning = "Unhealthy"
            AQI_health_implications = (
                "Everyone may begin to experience health effects; members of "
                "sensitive groups may experience more serious health effects."
            )
        elif 201 <= aqi <= 300:
            AQI_meaning = "Very Unhealthy"
            AQI_health_implications = (
                "Health warnings of emergency conditions. "
                "The entire population is more likely to be affected."
            )
        elif 301 <= aqi <= 500:
            AQI_meaning = "Hazardous"
            AQI_health_implications = (
                "Health alert: everyone may experience more serious health effects."
            )
        else:
            raise Exception(
                f"{aqi} is not valid air quality index value. "
                "Should be between 0 to 500."
            )

        return AQI_meaning, AQI_health_implications

    def _locate_all_coordinates(
        self, lower_bound: Tuple[float, float], upper_bound: Tuple[float, float]
    ) -> List[Tuple]:
        """Get all locations between two pair of coordinates

        Args:
            lower_bound (tuple): start location
            upper_bound (tuple): end location

        Returns:
           list: a list of all coordinates located between lower_bound and
           upper_bound. If API request fails then returns [(-1, -1)].
        """

        coordinates_flattened: List[float] = list(
            itertools.chain(lower_bound, upper_bound)
        )
        latlng: str = ",".join(map(str, coordinates_flattened))
        response = self._make_api_request(
            f"{URLs.find_coordinates_url}bounds/?token={self.token}&latlng={latlng}"
        )

        self._check_status_code(response)

        data = json.loads(response.content)["data"]
        coordinates: List[Tuple] = [
            (element["lat"], element["lon"]) for element in data
        ]
        return coordinates

        # This is a bit of a hack to ensure that the function always returns a
        # list of coordinates. Required to make mypy happy.

        # Return an invalid coordinate if API request fails.
        return [(-1, -1)]

    def get_coordinate_air(
        self,
        lat: float,
        lon: float,
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get a location's air quality data by latitude and longitude

        Args:
            lat (float): Latitude
            lon (float): Longitude
            data_format (str): File format for data. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            df (pandas.DataFrame, optional): An existing dataframe to
                append the data to.
            params (List[str], optional): A list of parameters to get data for.
            Gets all parameters by default.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
            (If you selected another data format, this dataframe will be empty)
        """
        if params == [""]:
            params = self._default_params

        r = self._make_api_request(
            f"{self._search_aqi_url}/geo:{lat};{lon}/?token={self.token}"
        )
        row = self._get_parsed_data_row_dict(r, params=params)
        df = pandas.concat([df, pandas.DataFrame([row])], ignore_index=True)
        return self._format_output(data_format, df)

    def get_city_air(
        self,
        city: str,
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get a city's air quality data

        Args:
            city (str): The city to get data for.
            data_format (str): File format for data. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            df (pandas.DataFrame, optional): An existing dataframe to
                append the data to.
            params (List[str], optional): A list of parameters to get data for.
            Gets all parameters by default.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
            (If you selected another data format, this dataframe will be empty)
        """
        if params == [""]:
            params = self._default_params

        r = self._make_api_request(f"{self._search_aqi_url}/{city}/?token={self.token}")
        row = self._get_parsed_data_row_dict(r, city, params)
        df = pandas.concat([df, pandas.DataFrame([row])], ignore_index=True)
        return self._format_output(data_format, df)

    def _get_parsed_data_row_dict(
        self, r: requests.Response, city: str = "N/A", params: List[str] = [""]
    ) -> dict:
        self._check_status_code(r)
        response = json.loads(r.content)

        status = response.get("status")
        data = response.get("data")

        if status == "ok" and isinstance(data, dict):
            return self._parse_data(data, city, params)

        if isinstance(data, str):
            if "Unknown station" in data:
                # Usually happens when WAQI does not have a station
                # for the searched city name.
                raise Exception(f'There is no known AQI station for the city "{city}"')

            if "Invalid geo position" in data:
                # Usually happens when WAQI can't parse the given
                # lat-lon coordinate.

                # data is fortunately already informative
                raise Exception(f"{data}")

            if "Invalid key" in data:
                raise Exception("Your API token is invalid.")

            # Unlikely since rate limiter is already used,
            # but included anyway for completeness.
            if "Over quota" in data:
                raise Exception("Too many requests within short time.")

        # Catch-all exception for other not yet known cases
        raise Exception(
            f'There is a problem with city "{city}", '
            f"the returned response: {response}"
        )

    def get_multiple_coordinate_air(
        self,
        locations: List[Tuple],
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get multiple locations air quality data

        Args:
            locations (list): A list of pair (latitude,longitude) to get data for.
            data_format (str): File format. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            df (pandas.DataFrame, optional): An existing dataframe to
                append the data to.
            params (List[str], optional): A list of parameters to get data for.
            Gets all parameters by default.

        Returns:
            pandas.DataFrame: The dataframe containing the data. (If you
            selected another data format, this dataframe will be empty)
        """
        for loc in locations:
            # This just makes sure that it's always a returns a pandas.DataFrame.
            # Makes mypy happy.
            df = pandas.DataFrame(
                self.get_coordinate_air(loc[0], loc[1], df=df, params=params)
            )

        df.reset_index(inplace=True, drop=True)
        return self._format_output(data_format, df)

    def get_range_coordinates_air(
        self,
        lower_bound: Tuple[float, float],
        upper_bound: Tuple[float, float],
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get air quality data for range of coordinates between lower_bound and upper_bound

        Args:
            lower_bound (tuple): start coordinate
            upper_bound (tuple): end coordinate
            data_format (str): File format. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            df (pandas.DataFrame, optional): An existing dataframe to
                append the data to.
            params (List[str], optional): A list of parameters to get data for.
            Gets all parameters by default.

        Returns:
            pandas.DataFrame: The dataframe containing the data. (If you
            selected another data format, this dataframe will be empty)
        """
        locations = self._locate_all_coordinates(
            lower_bound=lower_bound, upper_bound=upper_bound
        )
        return self.get_multiple_coordinate_air(
            locations, data_format=data_format, df=df, params=params
        )

    def get_multiple_city_air(
        self,
        cities: List[str],
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
        params: List[str] = [""],
    ) -> pandas.DataFrame:
        """Get multiple cities' air quality data

        Args:
            cities (list): A list of cities to get data for.
            data_format (str): File format. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            params (List[str], optional): A list of parameters to get data for.
            Gets all parameters by default.
            df (pandas.DataFrame, optional): An existing dataframe to
                append the data to.

        Returns:
            pandas.DataFrame: The dataframe containing the data. (If you
            selected another data format, this dataframe will be empty)
        """
        for city in cities:
            # This just makes sure that it's always a returns a pandas.DataFrame.
            # Makes mypy happy.
            df = pandas.DataFrame(self.get_city_air(city=city, df=df, params=params))

        df.reset_index(inplace=True, drop=True)
        return self._format_output(data_format, df)

    def get_specific_parameter(
        self,
        city: str,
        air_param: str = "",
    ) -> float:
        """Get specific parameter as a float

        Args:
            city (string): A city to get the data for
            air_param (string): A string containing the specified air quality parameter.
            Gets all parameters by default.

        Returns:
            float: Value of the specified parameter for the given city.
        """
        r = self._make_api_request(f"{self._search_aqi_url}/{city}/?token={self.token}")
        row = self._get_parsed_data_row_dict(r, city, [air_param])

        try:
            result = float(row[air_param])
        except KeyError:
            raise Exception(
                f'Missing air quality parameter "{air_param}"\n'
                + 'Try another air quality parameters: "aqi", "no2", or "co"'
            )

        return result


if __name__ == "__main__":
    pass

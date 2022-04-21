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

import itertools
import json
import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import numpy
import pandas
import requests
from ratelimit import limits, sleep_and_retry

from .historical._reverse_engineered import get_data_from_id
from .urls import URLs

# 1000 calls per second is the limit allowed by API
CALLS: int = 1000
RATE_LIMIT: int = 1


class Ozone:
    """Primary class for Ozone API

    This class contains all the methods used for data collection.
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

        self.output_dir_path.mkdir(exist_ok=True)

        if data_format == "csv":
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

    def _extract_live_data(
        self, data_obj: Any, params: List[str] = [""]
    ) -> Dict[str, Union[str, float]]:
        """Extract live AQI data from API response's 'data' part.

        Args:
            data_obj (JSON object returned by json.loads): The 'data' part from
                the API's response.
            params (List[str]): The parameters to parse.

        Returns:
            dict: Dictionary containing the data.
        """
        if params == [""]:
            params = self._default_params

        # This dict will become a single row of data for the dataframe.
        row: Dict[str, Union[str, float]] = {}

        # City column can be added back later by the caller method.
        row["city"] = numpy.nan
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

    def _extract_forecast_data(self, data_obj: Any) -> pandas.DataFrame:
        """Extract forecast data from API response's 'data' part.

        Args:
            data_obj (JSON object returned by json.loads): The 'data' part from
                the API's response.

        Returns:
            pandas.DataFrame: A dataframe containing the data."""
        forecast = data_obj["forecast"]["daily"]
        dict_of_frames = {}
        for pol, lst in forecast.items():
            dict_of_frames[pol] = pandas.DataFrame(lst).set_index("day")

        df = pandas.concat(dict_of_frames, axis=1)
        df.index = pandas.to_datetime(df.index)
        return df

    def _check_and_get_data_obj(self, r: requests.Response, **check_debug_info) -> dict:
        """Get data object from API response and throw error if any is encouuntered

        Args:
            r (requests.Response): Response object from API request.
            **check_debug_info: Any debug info that can help make
                exceptions in this method more informative. Give this argument in
                format of e.g. `city="London"` to allow exceptions that can take
                city names to show it instead of just generic exception message.

        Returns:
            dict: The data object i.e. the `data` part of the API response,
                in dictionary format (already JSON-ified).

        """
        self._check_status_code(r)

        response = json.loads(r.content)
        status = response.get("status")
        data = response.get("data")

        if status == "ok" and isinstance(data, dict):
            return data

        if isinstance(data, str):
            if "Unknown station" in data:
                # Usually happens when WAQI does not have a station
                # for the searched city name.

                # Check if a city name is provided so that user can get
                # better exception message to aid them debug their program
                city = check_debug_info.get("city")
                city_info = f'\ncity: "{city}"' if city is not None else ""

                raise Exception(
                    "There is no known AQI station for the given query." + city_info
                )

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
        raise Exception(f"Can't parse the returned response:\n{response}")

    def _AQI_meaning(self, aqi: float) -> Tuple[str, str]:
        """Retrieve AQI meaning and health implications

        Args:
            aqi (float): Air Quality Index (AQI) value.

        Returns:
            str: The meaning and health implication of the AQI value.
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

        data = self._check_and_get_data_obj(response)

        coordinates: List[Tuple] = [
            (element["lat"], element["lon"]) for element in data
        ]
        return coordinates

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
                Choose from the following values:
                ["aqi", "pm25", "pm10", "o3", "co", "no2", "so2", "dew", "h",
                 "p", "t", "w", "wg"]
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
        data_obj = self._check_and_get_data_obj(r)

        row = self._extract_live_data(data_obj, params=params)
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
                Choose from the following values:
                ["aqi", "pm25", "pm10", "o3", "co", "no2", "so2", "dew", "h",
                 "p", "t", "w", "wg"]
                Gets all parameters by default.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
            (If you selected another data format, this dataframe will be empty)
        """
        if params == [""]:
            params = self._default_params

        r = self._make_api_request(f"{self._search_aqi_url}/{city}/?token={self.token}")
        data_obj = self._check_and_get_data_obj(r, city=city)  # City is for traceback

        row = self._extract_live_data(data_obj, params=params)
        row["city"] = city

        df = pandas.concat([df, pandas.DataFrame([row])], ignore_index=True)
        return self._format_output(data_format, df)

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
                Choose from the following values:
                ["aqi", "pm25", "pm10", "o3", "co", "no2", "so2", "dew", "h",
                 "p", "t", "w", "wg"]
                Gets all parameters by default..

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
                Choose from the following values:
                ["aqi", "pm25", "pm10", "o3", "co", "no2", "so2", "dew", "h",
                 "p", "t", "w", "wg"]
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
                Choose from the following values:
                ["aqi", "pm25", "pm10", "o3", "co", "no2", "so2", "dew", "h",
                 "p", "t", "w", "wg"]
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
                Choose from the following values:
                ["aqi", "pm25", "pm10", "o3", "co", "no2", "so2", "dew", "h",
                 "p", "t", "w", "wg"]
                Gets all parameters by default.

        Returns:
            float: Value of the specified parameter for the given city.
        """
        r = self._make_api_request(f"{self._search_aqi_url}/{city}/?token={self.token}")
        data_obj = self._check_and_get_data_obj(r)

        row = self._extract_live_data(data_obj, [air_param])

        try:
            result = float(row[air_param])
        except KeyError:
            raise Exception(
                f'Missing air quality parameter "{air_param}"\n'
                'Try another air quality parameters: "aqi", "no2", or "co"'
            )

        return result

    def get_city_station_options(self, city: str) -> pandas.DataFrame:
        """Get available stations for a given city
        Args:
            city (str): Name of a city.

        Returns:
            pandas.DataFrame: Table of stations and their relevant information.

        """
        # NOTE, HACK, FIXME:
        # This functionality was born together with historical data feature.
        # This endpoint is outside WAQI API's specification, thus not using
        # _check_and_get_data_obj private method above.
        # If exists, alternative within API's spec is more than welcome to
        # replace this implementation.
        r = requests.get(f"https://search.waqi.info/nsearch/station/{city}")
        res = r.json()

        city_id, country_code, station_name, city_url, score = [], [], [], [], []

        for candidate in res["results"]:
            city_id.append(candidate["x"])
            country_code.append(candidate["c"])
            station_name.append(candidate["n"])
            city_url.append(candidate["s"].get("u"))
            score.append(candidate["score"])

        return pandas.DataFrame(
            {
                "city_id": city_id,
                "country_code": country_code,
                "station_name": station_name,
                "city_url": city_url,
                "score": score,
            }
        ).sort_values(by=["score"], ascending=False)

    def get_historical_data(
        self, data_format: str = "df", *, city: str = None, city_id: int = None
    ) -> pandas.DataFrame:
        """Get historical air quality data for a city

        Args:
            data_format (str): File format. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            city (str): Name of the city. If given, the argument must be named.
            city_id (int): City ID. If given, the argument must be named.
                If not given, city argument must not be None.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
        """
        if city_id is None:
            if city is None:
                raise ValueError("If city_id is not specified, city must be specified.")

            # Take first search result
            search_result = self.get_city_station_options(city)
            if len(search_result) == 0:
                raise Exception(
                    f'The search for city "{city}" returns no result. It is possible '
                    "that the city does not have AQI station."
                )

            first_result = search_result.iloc[0, :]

            city_id = first_result["city_id"]
            station_name = first_result["station_name"]
            country_code = first_result["country_code"]

            warnings.warn(
                f'city_id was not supplied. Searching for "{city}" yields '
                f'city ID {city_id} with station name "{station_name}", '
                f'with country code "{country_code}". '
                "Ozone will return air quality data from that station. "
                "If you know this is not the correct city you intended, "
                "you can use get_city_station_options method first to "
                "identify the correct city ID."
            )

        df = get_data_from_id(city_id)
        return self._format_output(data_format, df)

    def get_city_forecast(
        self,
        city: str,
        data_format: str = "df",
        df: pandas.DataFrame = pandas.DataFrame(),
    ) -> pandas.DataFrame:
        """Get a city's air quality forecast

        Args:
            city (str): The city to get data for.
            data_format (str): File format for data. Defaults to 'df'.
                Choose from 'csv', 'json', 'xlsx'.
            df (pandas.DataFrame, optional): An existing dataframe to
                append the data to.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
            (If you selected another data format, this dataframe will be empty)"""
        r = self._make_api_request(f"{self._search_aqi_url}/{city}/?token={self.token}")
        data_obj = self._check_and_get_data_obj(r)

        df = self._extract_forecast_data(data_obj)
        return self._format_output(data_format, df)


if __name__ == "__main__":
    pass

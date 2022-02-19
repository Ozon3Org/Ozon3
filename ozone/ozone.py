import pandas
import requests
import json

from typing import Any, Dict, List, Union

from urls import URLs

# TODO: Add try-except blocks

class Ozone():
    _search_aqi_url: str = URLs.search_aqi_url
    _find_stations_url: str = URLs.find_stations_url
    _default_params: List[str] = [
        'aqi', 'pm25', 'pm10', 'o3', 'co', 'no2','so2', 'dew', 'h', 'p', 't', 'w', 'wg'
        ]

    def __init__(self, token: str = ''):
        self.token: str = token
        self._check_token_validity()
    
    # TODO: Fix this method
    def _check_token_validity(self) -> None:
        """Check if the token is valid
        """
        test_city: str = 'london'
        r = self._make_api_request(
            f'{self._search_aqi_url}/{test_city}/?token={self.token}'
            )

        if self._check_status_code(r):
            if json.loads(r.content)['status'] != 'ok':
                print('Warning: Token may be invalid!')

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
        if r.status_code == 200:
            return True
        elif r.status_code == 401:
            raise Exception('Unauthorized!')
        elif r.status_code == 404:
            raise Exception('Not Found!')
        elif r.status_code == 500:
            raise Exception('Internal Server Error!')
        return False

    def reset_token(self, token: str) -> None:
        """Use this method to set your API token

        Args:
            token (str): The new API token.
        """
        self.token = token
        self._check_token_validity()

    # TODO: add feature to allow for selective data retrieval.
    # make a seperate private method to deal with data parsing.
    def get_city_air(
            self,
            city: str,
            df: pandas.DataFrame = pandas.DataFrame(),
            params: List[str] = [''],
        ):
        if params == ['']:
            params = self._default_params

        r = self._make_api_request(
            f'{self._search_aqi_url}/{city}/?token={self.token}'
            )
        if self._check_status_code(r):
            # Get all the data.
            data_obj = json.loads(r.content)['data']
            row = self._parse_data(data_obj, city, params)
            df = df.append(row, ignore_index=True)
            # TODO: Don't use append. deprecated warning.
        
        return df

    def _parse_data(
        self,
        data_obj: Any,
        city: str,
        params: List[str]
        ) -> Dict[str, Union[str, float]]:
        """Parse the data from the API response

        Args:
            data_obj (dict): The data from the API response.

        Returns:
            dict: The parsed data.
        """
        # A single row of data for the dataframe.
        row: Dict[str, Union[str, float]] = {} 
        
        try:
            row['city'] = f'{city}'
            row['city_coord'] = data_obj['city']['geo']
            row['station'] = data_obj['city']['name']

            row['dominant_pollutant'] = data_obj['dominentpol']

            row['timestamp'] = data_obj['time']['s']
            row['timestamp_timezone'] = data_obj['time']['tz']
            
            if 'aqi' in params:
                row['aqi'] = float(data_obj['aqi'])
                params.remove('aqi')
            
            for param in params:
                row[param] = float(data_obj['iaqi'][param]['v'])
        except KeyError:
            pass # TODO: Add exception handling.

        return row

if __name__ == '__main__':
    test = Ozone(token = '0e0fc4695a0a368fc63ae484dcbfb58953a20985')
    print(test.get_city_air('london'))
import pandas
import requests
import json

from urls import URLs

# TODO: Add try-except blocks

class Ozone():
    _search_aqi_url: str = URLs.search_aqi_url
    _find_stations_url: str = URLs.find_stations_url

    def __init__(self, token: str = ''):
        self.token: str = token
        self._check_token_validity()
    
    # TODO: Fix this method
    def _check_token_validity(self) -> None:
        test_city: str = 'london'
        r = self._make_api_request(f'{self._search_aqi_url}/{test_city}/?token={self.token}')

        if self._check_status_code(r):
            if json.loads(r.content)['status'] != 'ok':
                print('Warning: Token may be invalid!')

    def _make_api_request(self, url: str) -> requests.Response:
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
            token (str): _description_
        """
        self.token = token
        self._check_token_validity()

    def get_city_air(
            self,
            city: str,
            df: pandas.DataFrame = pandas.DataFrame(),
        ):
        """Get the air quality of a city

        Args:
            city (str): The name of the city
            df (pandas.DataFrame, optional): Existing dataframe, if one exists. Defaults to new empty pandas.DataFrame().

        Returns:
            pandas.DataFrame: The dataframe containing the air quality of the city
        """
        r = self._make_api_request(f'{self._search_aqi_url}/{city}/?token={self.token}')
        if self._check_status_code(r):
            # Get all the data.
            data_obj = json.loads(r.content)['data']



if __name__ == '__main__':
    pass
    # test = Ozone('')
    # print(test._check_token_validity())
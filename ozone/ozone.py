import pandas
import requests
import json
from urls import URLs

class Ozone():
    _search_aqi_url: str = URLs.search_aqi_url
    _find_stations_url: str = URLs.find_stations_url

    def __init__(self, token: str = ''):
        self.token: str = token

        self._check_token_validity()
    
    def _check_token_validity(self) -> None:
        city_for_check: str = 'london'
        url: str = f'{self._search_aqi_url}/{city_for_check}/?token={self.token}'
        r = requests.get(url)
        if json.loads(r.content)['status'] != 'ok':
            print('Warning: Token may be invalid!')

    def reset_token(self, token: str) -> None:
        """Use this method to set your API token

        Args:
            token (str): _description_
        """
        self.token = token
        self._check_token_validity()


    # Needs to have method to get aqi data for city in 


if __name__ == '__main__':
    pass
    # test = Ozone('')
    # print(test._check_token_validity())
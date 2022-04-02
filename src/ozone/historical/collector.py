import functools
import warnings
import requests
import pandas

from ._reverse_engineered import get_data_from_id

def get_search_results(city: str):
    r = requests.get(f"https://search.waqi.info/nsearch/station/{city}")
    res = r.json()

    city_id, country_code, station_name, city_url, score = [], [], [], [], []

    for candidate in res['results']:
        city_id.append(candidate['x'])
        country_code.append(candidate['c'])
        station_name.append(candidate['n'])
        city_url.append(candidate['s']['u'])
        score.append(candidate['score'])

    return pandas.DataFrame({
        'city_id': city_id,
        'country_code': country_code,
        'station_name': station_name,
        'city_url': city_url,
        'score': score
    }).sort_values(by=['score'], ascending=False)

@functools.lru_cache(maxsize=128)
def get_data(*, city: str = None, city_id: int = None):
    if city_id is None:
        if city is None:
            raise ValueError('If city_id is not supplied, city must be supplied.')

        # Take first search result
        result = get_search_results(city).iloc[0, :]

        city_id = result['city_id']
        station_name = result['station_name']

        warnings.warn(f'city_id not supplied, searching for "{city}" yields '
                      f'city ID {city_id} with station name "{station_name}".'
                      "Ozone will return air quality data from that station.")

    return get_data_from_id(city_id)

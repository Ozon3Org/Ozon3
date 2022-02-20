class URLs:

    # Base API endpoint.
    _base_url: str = "https://api.waqi.info/"

    # For air quality data search by location.
    search_aqi_url: str = f"{_base_url}feed/"

    # For search for air quality measuring stations in area.
    find_stations_url: str = f"{_base_url}search/"


if __name__ == "__main__":
    pass

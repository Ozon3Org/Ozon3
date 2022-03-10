from typing import Any, Dict, List, Union, Tuple
import datetime
import calendar
import itertools
import time
import os
import re

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def create_selenium_web_driver(headless: bool, verbosity: bool):
    if verbosity:
        os.environ['WDM_LOG_LEVEL'] = '0'

    opts = Options()
    opts.add_argument("--headless") if headless else None

    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=opts)
    browser.maximize_window()
    return browser


# model wide object for use by other scrapers
_SELENIUM_WEB_DRIVER = create_selenium_web_driver(headless=True, verbosity=True)


class DateOutOfRange(Exception):
    def __init__(self, message):
        super().__init__(message)


class AirDataHistory:

    def __init__(self, data: List[int], air_type: str, start_date: datetime.datetime, end_date: datetime.datetime):
        self.start_date: datetime.datetime = start_date
        self.end_date: datetime.datetime = end_date
        self.current_date: datetime.datetime = start_date
        self.data: List[int] = data
        self._air: str = air_type
        if (self.end_date - self.start_date).days + 1 != len(data):
            raise ValueError(" data values must be equal to the number of days")

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_date > self.end_date:
            raise StopIteration

        value = self.get_air_quality(self.current_date)
        self.current_date += datetime.timedelta(days=1)
        return value

    @property
    def air(self):
        return self._air

    def get_air_quality(self, date: datetime.datetime) -> int:
        """Get air quality value at specific date
        Args:
            date (datetime.datetime): The date to obtain data value for

        Returns:
            int: The air quality value at the specified date
        """

        if not (self.start_date <= date <= self.end_date):
            raise DateOutOfRange(f'Date passed as argument is not in valid range: '
                                 f'[{self.start_date} --> {self.end_date}] ')

        index = (date - self.start_date).days
        return self.data[index]


class AirHistoryScraper:
    _main_url: str = 'https://aqicn.org/data-platform/register/'
    allowed_gases = ["PM2.5",
                     "PM10",
                     "O3",
                     "NO2",
                     "SO2",
                     "CO"]
    _year_regular_expression = re.compile(r"^[1-3][0-9]{3}$")

    def __init__(self, web_driver: webdriver.Firefox = _SELENIUM_WEB_DRIVER):
        self.browser: webdriver.Firefox = web_driver
        self.browser.get(self._main_url)
        self.history_data: List[AirDataHistory] = []

    def handle_search_form(self, search_query: str):
        search_form = self.browser.find_element(By.XPATH, "//input[@class='prompt'][@placeholder='station or city']")
        search_form.send_keys(search_query)

        results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "result")))

        search_form.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        search_form.send_keys(Keys.ENTER)
        time.sleep(2)

    def get_table_and_buttons(self):
        sections = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='histui raised segment']")))

        # locate historical data section
        historical_section = sections[2]
        gases_header = historical_section.find_element(By.XPATH, ".//ul")

        # locate control buttons ( found at top of table, are used to control table)
        buttons = gases_header.find_elements(by=By.XPATH, value=".//*")
        air_button = buttons[0]

        # scroll the buttons into view for ability to click
        desired_y = (air_button.size['height'] / 2) + air_button.location['y']
        window_h = self.browser.execute_script('return window.innerHeight')
        window_y = self.browser.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        self.browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

        # locate table
        table = historical_section.find_element(By.XPATH, ".//table")

        return table, buttons

    def extract_from_table(self, table: WebElement, buttons: List[WebElement]):
        start_date = None

        end_year = datetime.datetime.now().year
        end_month = datetime.datetime.now().month
        end_date = datetime.datetime(end_year, end_month, calendar.monthrange(end_year, end_month)[1])

        data = {"PM2.5": [],
                "PM10": [],
                "O3": [],
                "NO2": [],
                "SO2": [],
                "CO": []}

        filtered_buttons = [button for button in buttons if button.text in self.allowed_gases]
        for button in filtered_buttons:
            print(f"fetching data for {button.text}")
            button.click()
            #time.sleep(2)
            table_rows = table.find_elements(By.XPATH, ".//tr[@style='display: table-row;']")
            if not start_date:
                year_rows = [table_row.text for table_row in table_rows if re.match(self._year_regular_expression,
                                                                                    table_row.text)]
                start_date = datetime.datetime(int(year_rows[len(year_rows) - 1]), 1, 1)

            filtered_table_rows = [table_row for table_row in table_rows if not re.match(self._year_regular_expression,
                                                                                         table_row.text)]
            for row in filtered_table_rows:
                cols = row.find_element(By.XPATH, ".//td[@class='squares']")
                values = cols.find_elements(By.XPATH, ".//*[name()='svg']/*[name()='text']")
                values = [int(value.text) if value.text != '-' else None for value in values]
                data[button.text].append(values)

        return data, start_date, end_date

    def execute(self, search_query: str)-> List[AirDataHistory]:
        """

        :param search_query:
        :return:
        """
        self.handle_search_form(search_query)
        table, buttons = self.get_table_and_buttons()
        data, start_date, end_date = self.extract_from_table(table, buttons)

        for air_type, table in data.items():
            flattened_table = list(itertools.chain(*table))
            self.history_data.append(AirDataHistory(flattened_table, air_type, start_date, end_date))

        return self.history_data


scraper = AirHistoryScraper()
data = scraper.execute("London")
for item in zip(*data):
    print(item)


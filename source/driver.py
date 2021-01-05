import getpass
import logging
import os
import pathlib
import random
import re
import requests
import shutil
import string
import subprocess

from abc import ABC, abstractmethod
from selenium import webdriver


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


class HttpGetResponse:
    def __init__(self, text, url, **kwargs):
        self.text = text
        self.url = url
        self.status_code = kwargs.get('status_code', None)


class Driver(ABC):
    def __init__(self, **kwargs):
        self.data_dir = kwargs.get('data_dir')
        self.timeout = kwargs.get('timeout')

    @abstractmethod
    def get(self, url) -> HttpGetResponse:
        pass


class SeleniumDriver(Driver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selenium_path = pathlib.Path('selenium').resolve()
        self.selenium_path.mkdir(exist_ok=True)
        self.driver_path = self.selenium_path / 'chromedriver'

        self.options = webdriver.ChromeOptions()
        self.options.page_load_strategy = 'eager'
        if getpass.getuser() == 'root':
            self.options.add_argument('--no-sandbox')  # required if root
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument(f'--user-agent="{user_agent}"')
        self.options.add_argument(f'--user-data-dir={self.selenium_path}')
        self.options.add_argument('--window-position=0,0')
        self.options.add_argument('--window-size=1920,1080')

    def get(self, url) -> HttpGetResponse:
        # headless chromium crashes somewhat regularly...
        # for now, we will start a fresh instance every time
        with webdriver.Chrome(executable_path="C:\\WebDrivers\\chromedriver.exe", options=self.options) as driver:
            driver.get(str(url))

            try:
                filename = self.data_dir / f'{url.nickname}.png'
                driver.save_screenshot(str(filename))
            except Exception as e:
                logging.warning(f'unable to save screenshot of webpage: {e}')

            return HttpGetResponse(driver.page_source, url)


class RequestsDriver(Driver):
    def get(self, url) -> HttpGetResponse:
        headers = {'user-agent': user_agent, 'referrer': 'https://google.com'}
        r = requests.get(str(url), headers=headers, timeout=self.timeout)
        if not r.ok:
            logging.debug(f'got response with status code {r.status_code} for {url}')
        return HttpGetResponse(r.text, r.url, status_code=r.status_code)


class DriverRepo:
    def __init__(self, timeout):
        self.data_dir = pathlib.Path('data').resolve()
        self.data_dir.mkdir(exist_ok=True)
        self.requests = RequestsDriver(data_dir=self.data_dir, timeout=timeout)
        self.selenium = SeleniumDriver(data_dir=self.data_dir, timeout=timeout)


def init_drivers():
    timeout = max(0, 15)  # in seconds
    return DriverRepo(timeout)

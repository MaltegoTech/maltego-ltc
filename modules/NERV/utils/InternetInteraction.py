import logging
import requests
import bs4
import os
import base64
from selenium import webdriver

from modules.NERV.config import DRIVER_PATH

log = logging.getLogger()


class Downloader:

    @classmethod
    def get_page_source(cls, url):
        try:
            page_source = cls._get_page_source_selenium(url)
        except Exception as e:
            log.error(f"Error using Selenium to retrieve page source: {e}")
            page_source = cls._get_page_source_requests(url)
        return bs4.BeautifulSoup(page_source, features="html.parser")

    @classmethod
    def _get_page_source_requests(cls, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @classmethod
    def _get_page_source_selenium(cls, url):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
        driver.get(url)
        return driver.page_source


if __name__ == '__main__':
    Downloader.get_page_source("http://google.com")
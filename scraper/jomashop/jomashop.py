from selectorlib import Extractor
from base import RESP_DEFAULT, ChromePath
import logging
import os
from selenium import webdriver

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.jomashop.com"


class Jomashop():
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Jomashop.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Jomashop.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Jomashop.__instance == None:
            Jomashop()
        return Jomashop.__instance

    @property
    def headers(self) -> dict:
        return {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self.dns,
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

    def product(self, url) -> dict:
        logging.info("Downloading {}".format(url))
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--no-sandbox")
        try:
            browser = webdriver.Chrome(ChromePath, options=options)
            browser.get(url)
            content = browser.page_source
        except Exception as e:
            logging.error(e)
        browser.close()
        try:
            return Jomashop.eP.extract(content)
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Jomashop Model"

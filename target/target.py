from selectorlib import Extractor
from base import RESP_DEFAULT, ChromePath
from selenium import webdriver
import logging
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.target.com"


class Target():
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Target.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Target.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Target.__instance == None:
            Target()
        return Target.__instance

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
            return Target.eP.extract(content)
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Target Model"

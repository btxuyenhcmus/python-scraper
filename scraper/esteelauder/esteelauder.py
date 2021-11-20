import logging
from urllib.parse import urljoin
from selectorlib import Extractor
from base import Base, RESP_DEFAULT, ChromePath
from selenium import webdriver
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.esteelauder.com"


class Esteelauder(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    eP2 = Extractor.from_yaml_file("{}/selector_product2.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Esteelauder.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Esteelauder.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Esteelauder.__instance == None:
            Esteelauder()
        return Esteelauder.__instance

    @property
    def UserAgent(self):
        return f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'

    def product(self, url) -> dict:
        logging.info("Downloading {}".format(url))
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--no-sandbox")
        options.add_argument(self.UserAgent)
        try:
            browser = webdriver.Chrome(ChromePath, options=options)
            browser.get(url)
            content = browser.page_source
        except Exception as e:
            logging.error(e)
        browser.close()
        try:
            if "/product" in url:
                resp = Esteelauder.eP2.extract(content)
                resp.update({
                    'image': urljoin(self.dns, resp["image"])
                })
                return resp
            resp = Esteelauder.eP.extract(content)
            resp.update({
                'image': urljoin(self.dns, resp["image"])
            })
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Esteelauder Model"

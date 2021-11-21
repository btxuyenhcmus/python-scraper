import logging
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.bhcosmetics.com"


class Bhcosmetics(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Bhcosmetics.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Bhcosmetics.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Bhcosmetics.__instance == None:
            Bhcosmetics()
        return Bhcosmetics.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('meta', property='og:image')
            resp = Bhcosmetics.eP.extract(html)
            resp.update({
                'image': title["content"],
                'price': resp["price_sale"] or resp["price"]
            })
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Bhcosmetics Model"

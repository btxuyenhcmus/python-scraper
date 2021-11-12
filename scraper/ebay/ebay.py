import logging
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.ebay.com"


class Ebay(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    ep2 = Extractor.from_yaml_file("{}/selector_product2.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Ebay.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Ebay.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Ebay.__instance == None:
            Ebay()
        return Ebay.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            if "/itm" in url:
                return Ebay.eP.extract(html)
            return Ebay.ep2.extract(html)
        except Exception as e:
            logging.error(e)
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Ebay Model"

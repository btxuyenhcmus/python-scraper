from selectorlib import Extractor
from base import Base
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.walmart.com"


class Walmart(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Walmart.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Walmart.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Walmart.__instance == None:
            Walmart()
        return Walmart.__instance

    def product(self, url) -> dict:
        return Walmart.eP.extract(super().product(url))

    def __str__(self) -> str:
        return "Walmart Model"

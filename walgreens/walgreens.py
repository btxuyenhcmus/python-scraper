from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.walgreens.com"


class Walgreens(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Walgreens.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Walgreens.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Walgreens.__instance == None:
            Walgreens()
        return Walgreens.__instance

    def product(self, url) -> dict:
        try:
            return Walgreens.eP.extract(super().product(url))
        except Exception as e:
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Walgreens Model"

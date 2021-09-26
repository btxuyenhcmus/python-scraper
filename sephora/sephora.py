from selectorlib import Extractor
from base import Base
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.sephora.com"


class Sephora(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Sephora.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Sephora.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Sephora.__instance == None:
            Sephora()
        return Sephora.__instance

    def product(self, url) -> dict:
        return Sephora.eP.extract(super().product(url))

    def __str__(self) -> str:
        return "Sephora Model"

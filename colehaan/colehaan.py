from selectorlib import Extractor
from base import Base
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.colehaan.com/"


class Colehaan(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Colehaan.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Colehaan.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Colehaan.__instance == None:
            Colehaan()
        return Colehaan.__instance

    def product(self, url) -> dict:
        return Colehaan.eP.extract(super().product(url))

    def __str__(self) -> str:
        return "Colehaan Model"

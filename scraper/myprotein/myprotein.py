import logging
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://us.myprotein.com"


class Myprotein(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Myprotein.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Myprotein.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Myprotein.__instance == None:
            Myprotein()
        return Myprotein.__instance

    def product(self, url) -> dict:
        try:
            return Myprotein.eP.extract(super().product(url))
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Myprotein Model"

import logging
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://us.pandora.net"


class UsPandora(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if UsPandora.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        UsPandora.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if UsPandora.__instance == None:
            UsPandora()
        return UsPandora.__instance

    def product(self, url) -> dict:
        try:
            return UsPandora.eP.extract(super().product(url))
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "UsPandora Model"

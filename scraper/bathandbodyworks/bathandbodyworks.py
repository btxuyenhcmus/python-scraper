import logging
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.bathandbodyworks.com"


class Bathandbodyworks(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Bathandbodyworks.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Bathandbodyworks.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Bathandbodyworks.__instance == None:
            Bathandbodyworks()
        return Bathandbodyworks.__instance

    def product(self, url) -> dict:
        try:
            resp = Bathandbodyworks.eP.extract(super().product(url))
            resp.update({
                'price': resp["saled"] or resp["notsaled"]
            })
            return resp
        except Exception as e:
            logging.error(e)
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Bathandbodyworks Model"

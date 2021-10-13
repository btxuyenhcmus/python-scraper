import logging
from urllib.parse import urljoin
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.gap.com"


class Gap(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Gap.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Gap.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Gap.__instance == None:
            Gap()
        return Gap.__instance

    def product(self, url) -> dict:
        try:
            resp = Gap.eP.extract(super().product(url))
            resp.update({
                'image': urljoin(self.dns, resp["image"])
            })
            return resp
        except Exception as e:
            logging.error(e)
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Gap Model"

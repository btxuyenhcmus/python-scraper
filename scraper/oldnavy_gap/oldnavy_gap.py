import logging
from urllib.parse import urljoin
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://oldnavy.gap.com"


class OldnavyGap(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if OldnavyGap.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        OldnavyGap.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if OldnavyGap.__instance == None:
            OldnavyGap()
        return OldnavyGap.__instance

    def product(self, url) -> dict:
        try:
            resp = OldnavyGap.eP.extract(super().product(url))
            resp.update({
                'image': urljoin(self.dns, resp["image"])
            })
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "OldnavyGap Model"

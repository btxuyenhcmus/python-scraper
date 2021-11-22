import logging
import re
import requests
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.ashford.com"


class Ashford(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    eS = Extractor.from_yaml_file("{}/selector_search.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Ashford.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Ashford.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Ashford.__instance == None:
            Ashford()
        return Ashford.__instance

    def product(self, url) -> dict:
        try:
            return Ashford.eP.extract(super().product(url))
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def search(self, keyword):
        logging.info("Searching {} for {}".format(keyword, self.dns))
        r = requests.get(
            self.dns + "/catalogsearch/result/?q={}".format(keyword), headers=self.headers)
        resp = Ashford.eS.extract(r.text)["products"]
        for idx in range(len(resp)):
            try:
                price = float(re.sub('[^.0-9]', '', resp[idx]["price"]))
            except Exception as e:
                price = None
            resp[idx].update({
                'price': price
            })
        return resp

    def __str__(self) -> str:
        return "Ashford Model"

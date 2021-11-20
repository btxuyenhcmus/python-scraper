import logging
from urllib.parse import urljoin
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
from flask import json
from bs4 import BeautifulSoup
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.hm.com"


class Hm(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Hm.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Hm.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Hm.__instance == None:
            Hm()
        return Hm.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[55:-9])
            resp = Hm.eP.extract(html)
            try:
                resp.update({
                    'price': data["offers"][0]["price"],
                    'image': urljoin(self.dns, data["image"]),
                    'product_description': data["description"],
                    'short_description': "{} - {}".format(data["sku"], data["color"])
                })
            except Exception as e:
                logging.debug(e)
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Hm Model"

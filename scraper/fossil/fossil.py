import logging
from selectorlib import Extractor
from bs4 import BeautifulSoup
from flask import json
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.fossil.com"


class Fossil(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Fossil.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Fossil.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Fossil.__instance == None:
            Fossil()
        return Fossil.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[40:-9])
            data = next(item for item in data if item["@type"] == 'Product')
            resp = Fossil.eP.extract(html)
            try:
                resp.update({
                    'name': data["name"],
                    'image': data["image"][0],
                    'price': data["offers"]["price"]
                })
            except Exception as e:
                logging.error(e)
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Fossil Model"

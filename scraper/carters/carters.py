import logging
from selectorlib import Extractor
from flask import json
from bs4 import BeautifulSoup
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.carters.com"


class Carters(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Carters.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Carters.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Carters.__instance == None:
            Carters()
        return Carters.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[35:-9])
            resp = Carters.eP.extract(html)
            try:
                resp.update({
                    'image': data["image"][0],
                    'name': data["name"],
                    'price': data["offers"]["price"],
                    'product_description': data["description"]
                })
            except Exception as e:
                logging.error(e)
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Carters Model"

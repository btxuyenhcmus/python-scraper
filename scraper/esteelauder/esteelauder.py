import logging
from urllib.parse import urljoin
from flask import json
from selectorlib import Extractor
from bs4 import BeautifulSoup
from base import Base, RESP_DEFAULT
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.esteelauder.com"


class Esteelauder(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    eP2 = Extractor.from_yaml_file("{}/selector_product2.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Esteelauder.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Esteelauder.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Esteelauder.__instance == None:
            Esteelauder()
        return Esteelauder.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            if "/product" in url:
                soup = BeautifulSoup(html, 'lxml')
                data = json.loads(
                    str(soup.find('script', type='application/ld+json'))[35:-9])
                resp = Esteelauder.eP2.extract(html)
                try:
                    resp.update({
                        'name': data["name"],
                        'image': data["image"],
                        'price': data["offers"][0]["price"]
                    })
                except Exception as e:
                    logging.error(e)
                return resp
            resp = Esteelauder.eP.extract(html)
            resp.update({
                'image': urljoin(self.dns, resp["image"])
            })
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Esteelauder Model"

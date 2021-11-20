import logging
from urllib.parse import urljoin
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup
from flask import json
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.Fragrancenet.com"


class Fragrancenet(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Fragrancenet.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Fragrancenet.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Fragrancenet.__instance == None:
            Fragrancenet()
        return Fragrancenet.__instance

    def product(self, url) -> dict:
        try:
            sku = url.split('#')[-1]
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[35:-9])
            data = next(it for it in data if it["sku"] == sku)
            resp = Fragrancenet.eP.extract(html)
            try:
                resp.update({
                    'name': data["name"],
                    'price': data["offers"]["price"],
                    'image': urljoin('https://', data["image"].split('//')[-1])
                })
            except Exception as e:
                logging.error(e)
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Fragrancenet Model"

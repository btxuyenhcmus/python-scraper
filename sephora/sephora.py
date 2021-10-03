from selectorlib import Extractor
from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup
from flask import json
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.sephora.com"


class Sephora(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Sephora.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Sephora.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Sephora.__instance == None:
            Sephora()
        return Sephora.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find_all('script', type='application/ld+json')[2])[35:-9])
            resp = Sephora.eP.extract(html)
            try:
                resp.update({
                    'product_description': data["description"],
                    'image': data["image"][0]
                })
            except Exception as e:
                pass
            return resp
        except Exception as e:
            print(e)
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Sephora Model"

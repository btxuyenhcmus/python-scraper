import logging
from selectorlib import Extractor
from werkzeug.utils import html
from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup
from flask import json
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.adidas.com"


class Adidas(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Adidas.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Adidas.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Adidas.__instance == None:
            Adidas()
        return Adidas.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[50:-9])
            resp = Adidas.eP.extract(html)
            try:
                resp.update({
                    'name': data["name"],
                    'price': data["offers"]["price"],
                    'image': data["image"][0],
                    'number_of_reviews': data["aggregateRating"]["reviewCount"],
                    'rating': data["aggregateRating"]["ratingValue"],
                    'product_description': data["description"]
                })
            except Exception as e:
                logging.error(e)
            return resp
        except Exception as e:
            logging.error(e)
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Adidas Model"

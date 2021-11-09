import logging
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup
from flask import json
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.lacoste.com"


class Lacoste(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Lacoste.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Lacoste.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Lacoste.__instance == None:
            Lacoste()
        return Lacoste.__instance

    def product(self, url) -> dict:
        try:
            html = super().product(url)
            soup = BeautifulSoup(html, 'lxml')
            data = json.loads(
                str(soup.find_all('script', type='application/ld+json')[1])[35:-9])
            resp = Lacoste.eP.extract(html)
            try:
                resp.update({
                    'image': data["image"],
                    'short_description': data["description"],
                    'number_of_reviews': data["aggregateRating"]["ratingCount"],
                    'rating': data["aggregateRating"]["ratingValue"]
                })
            except Exception as e:
                logging.error(e)
            return resp
        except Exception as e:
            logging.error(e)
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Lacoste Model"

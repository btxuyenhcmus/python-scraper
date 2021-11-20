import logging
from flask import json
from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup


DNS_WEB = "https://www.goat.com"


class Goat(Base):
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Goat.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Goat.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Goat.__instance == None:
            Goat()
        return Goat.__instance

    def product(self, url) -> dict:
        try:
            soup = BeautifulSoup(super().product(url), 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[38:-10])
            return {
                'name': data["name"],
                'image': data["image"],
                'product_description': data["description"],
                'short_description': "{};{};{}".format(data["brand"], data["sku"], data["color"]),
                'price': data["offers"]["lowPrice"]
            }
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Goat Model"

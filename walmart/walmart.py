from base import Base, RESP_DEFAULT
from bs4 import BeautifulSoup
from flask import json

DNS_WEB = "https://www.walmart.com"


class Walmart(Base):
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Walmart.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Walmart.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Walmart.__instance == None:
            Walmart()
        return Walmart.__instance

    def product(self, url) -> dict:
        try:
            soup = BeautifulSoup(super().product(url), 'lxml')
            data = json.loads(
                str(soup.find('script', type='application/ld+json'))[60:-9])
            return {
                'name': data["name"],
                'price': data["offers"]["price"],
                'image': data["image"],
                'number_of_reviews': data["aggregateRating"]["reviewCount"],
                'rating': data["aggregateRating"]["ratingValue"],
                'product_description': data["description"],
                'short_description': "{} - {}".format(data["sku"], data["gtin13"])
            }
        except Exception as e:
            return RESP_DEFAULT

    def __str__(self) -> str:
        return "Walmart Model"

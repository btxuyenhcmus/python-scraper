import logging
import re
from urllib.parse import urljoin
from selectorlib import Extractor
from base import Base, RESP_DEFAULT
import requests
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.amazon.com"


class Amazon(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    eS = Extractor.from_yaml_file("{}/selector_search.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Amazon.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Amazon.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Amazon.__instance == None:
            Amazon()
        return Amazon.__instance

    def product(self, url) -> dict:
        try:
            resp = Amazon.eP.extract(super().product(url))
            resp.update({
                'price': resp["price"] or resp["price_deal"]
            })
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def search(self, keyword):
        logging.info("Searching {} for {}".format(keyword, self.dns))
        r = requests.get(self.dns + "/s?k={}".format(keyword),
                         headers=self.headers)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print(
                    "Page was blocked by Amazon. Please try using better proxies\n")
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d" % (
                    self.dns + "/s?k={}".format(keyword), r.status_code))
            return []
        resp = Amazon.eS.extract(r.text)["products"]
        for idx in range(len(resp)):
            try:
                price = float(re.sub('[^.0-9]', '', resp[idx]["price"]))
            except Exception as e:
                price = None
            try:
                original_price = float(
                    re.sub('[^.0-9]', '', resp[idx]["original_price"]))
            except Exception as e:
                original_price = None
            try:
                reviews = int(re.sub('[^.0-9]', '', resp[idx]["reviews"]))
            except Exception as e:
                reviews = 0
            try:
                ratings = resp[idx]["rating"].split(' ')
                rating = (float(ratings[0]), float(ratings[3]))
            except Exception as e:
                rating = (0, 0)
            try:
                off = round((original_price - price) / original_price * 100)
            except Exception as e:
                off = None
            resp[idx].update({
                'url': urljoin(self.dns, resp[idx]["url"]),
                'price': price,
                'original_price': original_price,
                'reviews': reviews,
                'rating': rating,
                'off': off
            })
        return resp

    def __str__(self) -> str:
        return "Amazon Model"

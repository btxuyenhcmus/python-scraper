import logging
from selectorlib import Extractor
import requests
from base import Base, RESP_DEFAULT
import os
from dotenv import load_dotenv

load_dotenv()

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.belk.com"


class Belk(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Belk.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Belk.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Belk.__instance == None:
            Belk()
        return Belk.__instance

    def product(self, url) -> dict:
        try:
            logging.info("Downloading {}".format(url))
            proxyDict = {
                'http': os.getenv('HTTP_PROXY'),
                'https': os.getenv('HTTPS_PROXY')
            }
            r = requests.get(url, headers=self.headers,
                             timeout=10, proxies=proxyDict)
            if r.status_code > 500:
                if "To discuss automated access to Website data please contact" in r.text:
                    print(
                        "Page %s was blocked by Website. Please try using better proxies\n" % url)
                else:
                    print("Page %s must have been blocked by Website as the status code was %d" % (
                        url, r.status_code))
                return {}
            resp = Belk.eP.extract(r.text)
            resp.update({
                'price': resp["price"] or resp["price_standard"]
            })
            return resp
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Belk Model"

from selectorlib import Extractor
import requests
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.adidas.com"


class Adidas():
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

    @property
    def headers(self) -> dict:
        return {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self.dns,
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

    def product(self, url) -> dict:
        print("Downloading {}".format(url))
        r = requests.get(url, headers=self.headers)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print(
                    "Page %s was blocked by Amazon. Please try using better proxies\n" % url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d" % (
                    url, r.status_code))
            return {}
        return Adidas.eP.extract(r.text)

    def __str__(self) -> str:
        return "Adidas"

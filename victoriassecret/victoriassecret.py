from selectorlib import Extractor
from pyppeteer import launch
from base import RESP_DEFAULT
from contextlib import suppress
from urllib.parse import urljoin
import asyncio
import logging
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.victoriassecret.com"


class Victoriassecret():
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Victoriassecret.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Victoriassecret.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Victoriassecret.__instance == None:
            Victoriassecret()
        return Victoriassecret.__instance

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

    async def product(self, url) -> dict:
        logging.info("Downloading {}".format(url))
        browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, args=['--no-sandbox'])
        page = await browser.newPage()
        with suppress(asyncio.CancelledError):
            try:
                await page.setViewport(dict(width=2600, height=1200))
                await page.goto(url)
                await page.waitForSelector('h1.fabric-purchasable-product-component-short-description')
                content = await page.content()
            except Exception as e:
                logging.error(e)
                return RESP_DEFAULT
        await page.close()
        await browser.close()
        resp = Victoriassecret.eP.extract(content)
        resp.update({
            'image': urljoin(Victoriassecret.__instance.dns, resp["image"])
        })
        return resp

    def __str__(self) -> str:
        return "Victoriassecret"

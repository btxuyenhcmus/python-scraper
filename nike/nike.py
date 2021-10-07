from selectorlib import Extractor
from pyppeteer import launch
from contextlib import suppress
from base import RESP_DEFAULT, VIEW_DEFAULT
import asyncio
import logging
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.nike.com"


class Nike():
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Nike.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Nike.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Nike.__instance == None:
            Nike()
        return Nike.__instance

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
        browser = await launch(ignoreHTTPSErrors=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, args=['--no-sandbox'], defaultViewport=VIEW_DEFAULT)
        page = await browser.newPage()
        with suppress(asyncio.CancelledError):
            try:
                await page.goto(url)
                await page.waitForSelector('div.prl0-sm h1.headline-2')
                content = await page.content()
            except Exception as e:
                logging.error(e)
        await page.close()
        await browser.close()
        try:
            return Nike.eP.extract(content)
        except Exception as e:
            logging.error(e)
        return RESP_DEFAULT

    def __str__(self) -> str:
        return "Nike Model"

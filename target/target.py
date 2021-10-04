from selectorlib import Extractor
from base import Base, RESP_DEFAULT
from pyppeteer import launch
from contextlib import suppress
import logging
import asyncio
import os

pathfile = os.path.dirname(os.path.realpath(__file__))
DNS_WEB = "https://www.target.com"


class Target(Base):
    eP = Extractor.from_yaml_file("{}/selector_product.yml".format(pathfile))
    __instance = None

    def __init__(self, dns=DNS_WEB) -> None:
        if Target.__instance != None:
            raise Exception("This is singleton class!!")
        self.dns = dns
        Target.__instance = self

    @staticmethod
    def getInstance() -> object:
        """This is static method be called by class"""
        if Target.__instance == None:
            Target()
        return Target.__instance

    async def product(self, url) -> dict:
        logging.info("Downloading {}".format(url))
        browser = await launch(ignoreHTTPSErrors=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, args=['--no-sandbox'], width=2600, height=1200)
        page = await browser.newPage()
        with suppress(asyncio.CancelledError):
            try:
                await page.goto(url)
                await page.waitForSelector('h1.Heading__StyledHeading-sc-1mp23s9-0 span')
                content = await page.content()
            except Exception as e:
                logging.error(e)
                return RESP_DEFAULT
        await page.close()
        await browser.close()
        return Target.eP.extract(content)

    def __str__(self) -> str:
        return "Target Model"

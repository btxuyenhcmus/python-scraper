import requests
import logging
import random
from webdriver_manager.chrome import ChromeDriverManager

RESP_DEFAULT = {
    'name': None,
    'price': '',
    'short_description': None,
    'number_of_reviews': None,
    'rating': None,
    'product_description': None,
    'image': None
}

VIEW_DEFAULT = dict(width=1600, height=1200)
ChromePath = ChromeDriverManager().install()
userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
]


class Base():
    @property
    def headers(self) -> dict:
        return {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': random.choice(userAgents),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': self.dns,
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cookie': 'dwac_a7c84d4f15b4d916c6e435eec4=B07UHxU1UpuFCuKxpuVKNQ4cZTErb2tkJZg%3D|dw-only|||USD|false|US%2FEastern|true; cqcid=bcw7fKOtc7VMzRXsNNDgJNNuda; cquid=||; returningCustomer=true; sid=B07UHxU1UpuFCuKxpuVKNQ4cZTErb2tkJZg; dwanonymous_ad738289b685e74f02aa9af5870b8177=bcw7fKOtc7VMzRXsNNDgJNNuda; _pxhd=lvO2xyxmDgcCg6cEoYSoWs7RKnRyR/RzUNOD7BLXA0nVf6D7vQrWwkQ9lhjsX6Kjng8mNU/zZkCldZvibI6c5A==:L2782goopdmgJYClzawO7/FmdaXjCTVgxQ-T4Q30c0F6-HLBF/Y6H/oAj8viEcid3xp0eNVJhDAkOGyHOYy15EMQGKRsKnJlYPswxHX9iKk=; __cq_dnt=0; dw_dnt=0; dwsid=VKjFgF70sJH73t-aWN_sfF36dK5groluW0yeGuBxAkY2ls1HqA8oZmBjeg9M6ub5ST5g6IfY3DuArbeTPKjt-Q=='
        }

    def product(self, url) -> dict:
        logging.info("Downloading {}".format(url))
        r = requests.get(url, headers=self.headers, timeout=10)
        if r.status_code > 500:
            if "To discuss automated access to Website data please contact" in r.text:
                print(
                    "Page %s was blocked by Website. Please try using better proxies\n" % url)
            else:
                print("Page %s must have been blocked by Website as the status code was %d" % (
                    url, r.status_code))
            return {}
        return r.text

    def __str__(self) -> str:
        return "Base Model"

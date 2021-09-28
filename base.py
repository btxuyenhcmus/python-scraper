import requests


RESP_DEFAULT = {
    'name': None,
    'price': '',
    'short_description': None,
    'number_of_reviews': None,
    'rating': None,
    'product_description': None,
    'image': None
}


class Base():
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
            'Cookie': 'dwac_a7c84d4f15b4d916c6e435eec4=B07UHxU1UpuFCuKxpuVKNQ4cZTErb2tkJZg%3D|dw-only|||USD|false|US%2FEastern|true; cqcid=bcw7fKOtc7VMzRXsNNDgJNNuda; cquid=||; returningCustomer=true; sid=B07UHxU1UpuFCuKxpuVKNQ4cZTErb2tkJZg; dwanonymous_ad738289b685e74f02aa9af5870b8177=bcw7fKOtc7VMzRXsNNDgJNNuda; _pxhd=lvO2xyxmDgcCg6cEoYSoWs7RKnRyR/RzUNOD7BLXA0nVf6D7vQrWwkQ9lhjsX6Kjng8mNU/zZkCldZvibI6c5A==:L2782goopdmgJYClzawO7/FmdaXjCTVgxQ-T4Q30c0F6-HLBF/Y6H/oAj8viEcid3xp0eNVJhDAkOGyHOYy15EMQGKRsKnJlYPswxHX9iKk=; __cq_dnt=0; dw_dnt=0; dwsid=VKjFgF70sJH73t-aWN_sfF36dK5groluW0yeGuBxAkY2ls1HqA8oZmBjeg9M6ub5ST5g6IfY3DuArbeTPKjt-Q=='
        }

    def product(self, url) -> dict:
        print("Downloading {}".format(url))
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

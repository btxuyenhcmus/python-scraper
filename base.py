import requests


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
        }

    def product(self, url) -> dict:
        print("Downloading {}".format(url))
        r = requests.get(url, headers=self.headers)
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

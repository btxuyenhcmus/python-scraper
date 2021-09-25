from walmart import Walmart
import asyncio
import json


webWalmart = Walmart.getInstance()


if __name__ == '__main__':
    print(json.dumps(webWalmart.product(
        "https://www.walmart.com/ip/Athletic-Works-Women-s-Core-Active-Dri-Works-Skort/56248798?athbdg=L1600"), indent=4, sort_keys=True))

import asyncio
from colehaan.colehaan import Colehaan
import json


web = Colehaan.getInstance()

if __name__ == '__main__':
    print(json.dumps(web.product(
        "https://www.colehaan.com/grand-ambition-postman-oxford-british-tan/C34110.html?cta=cityguidepek"), indent=4, sort_keys=True))

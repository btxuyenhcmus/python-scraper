from flask import Blueprint, json
from flask import request, jsonify
from urllib.parse import urlparse
from base import Base
from walmart import Walmart
from adidas import Adidas
from amazon import Amazon
from ashford import Ashford
from colehaan import Colehaan
from sephora import Sephora
from coachoutlet import Coachoutlet
from ebay import Ebay
from goat import Goat
from maccosmetics import Maccosmetics
from lacoste import Lacoste
from tommy import Tommy
from colourpop import Colourpop
from jomashop import Jomashop
from nike import Nike
from target import Target
from us_puma import UsPuma
from walgreens import Walgreens
from kiehls import Kiehls
import asyncio
import re
import logging


scraper = Blueprint('scraper', __name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

REQUEST_WEB = {
    'www.walmart.com': Walmart.getInstance(),
    'www.adidas.com': Adidas.getInstance(),
    'www.amazon.com': Amazon.getInstance(),
    'www.ashford.com': Ashford.getInstance(),
    'www.colehaan.com': Colehaan.getInstance(),
    'www.sephora.com': Sephora.getInstance(),
    'www.coachoutlet.com': Coachoutlet.getInstance(),
    'www.ebay.com': Ebay.getInstance(),
    'www.goat.com': Goat.getInstance(),
    'www.maccosmetics.com': Maccosmetics.getInstance(),
    'www.lacoste.com': Lacoste.getInstance(),
    'usa.tommy.com': Tommy.getInstance(),
    'colourpop.com': Colourpop.getInstance()

}

PYPPETEER_WEB = {
    'www.jomashop.com': Jomashop.getInstance(),
    'www.nike.com': Nike.getInstance(),
    'www.target.com': Target.getInstance(),
    'us.puma.com': UsPuma.getInstance(),
    'www.walgreens.com': Walgreens.getInstance(),
    'www.kiehls.com': Kiehls.getInstance()
}


@ scraper.route('/', methods=['POST'])
def get():
    url = json.loads(request.data)["link"]
    parse_obj = urlparse(url)
    web, response = Base, {}
    if parse_obj.netloc in REQUEST_WEB:
        web = REQUEST_WEB.get(parse_obj.netloc, Base)
        response = web.product(url)
    if parse_obj.netloc in PYPPETEER_WEB:
        web = PYPPETEER_WEB.get(parse_obj.netloc, Base)
        response = loop.run_until_complete(web.product(url))
    try:
        response.update({
            'price': float(re.sub('[^.0-9]', '', response["price"]))
        })
    except Exception as e:
        logging.error(e)
    return jsonify(response)

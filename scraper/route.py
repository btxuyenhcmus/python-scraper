from flask import Blueprint, json
from flask import request, jsonify
from urllib.parse import urlparse
from base import Base
from flask_redis import FlaskRedis
from levi.levi import Levi
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
from victoriassecret import Victoriassecret
from bathandbodyworks import Bathandbodyworks
from guessfactory import Guessfactory
from calvinklein import Calvinklein
from macys import Macys
from overstock import Overstock
from bestbuy import Bestbuy
from us_pandora import UsPandora
from fentybeauty import Fentybeauty
from belk import Belk
from hm import Hm
from saksoff5th import Saksoff5th
from patmcgrath import Patmcgrath
from sixpm import SixPm
from gap import Gap
from oldnavy_gap import OldnavyGap
from ssense import Ssense
from carters import Carters
from urbanoutfitters import Urbanoutfitters
from myprotein import Myprotein
from guess import Guess
from dsw import Dsw
from michaelkors import Michaelkors
from swarovski import Swarovski
from lasenza import Lasenza
from reebok import Reebok
import re
import logging


scraper = Blueprint('scraper', __name__)
redis_client = FlaskRedis()

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
    'colourpop.com': Colourpop.getInstance(),
    'www.bathandbodyworks.com': Bathandbodyworks.getInstance(),
    'www.guessfactory.com': Guessfactory.getInstance(),
    'www.calvinklein.us': Calvinklein.getInstance(),
    'www.overstock.com': Overstock.getInstance(),
    'www.bestbuy.com': Bestbuy.getInstance(),
    'us.pandora.net': UsPandora.getInstance(),
    'fentybeauty.com': Fentybeauty.getInstance(),
    'www.belk.com': Belk.getInstance(),
    'www.hm.com': Hm.getInstance(),
    'www2.hm.com': Hm.getInstance(),
    'www.saksoff5th.com': Saksoff5th.getInstance(),
    'www.levi.com': Levi.getInstance(),
    'www.patmcgrath.com': Patmcgrath.getInstance(),
    'www.6pm.com': SixPm.getInstance(),
    'www.gap.com': Gap.getInstance(),
    'oldnavy.gap.com': OldnavyGap.getInstance(),
    'www.ssense.com': Ssense.getInstance(),
    'www.carters.com': Carters.getInstance(),
    'www.urbanoutfitters.com': Urbanoutfitters.getInstance(),
    'us.myprotein.com': Myprotein.getInstance(),
    'www.jomashop.com': Jomashop.getInstance(),
    'www.nike.com': Nike.getInstance(),
    'www.target.com': Target.getInstance(),
    'us.puma.com': UsPuma.getInstance(),
    'www.walgreens.com': Walgreens.getInstance(),
    'www.kiehls.com': Kiehls.getInstance(),
    'www.victoriassecret.com': Victoriassecret.getInstance(),
    'www.guess.com': Guess.getInstance(),
    'www.dsw.com': Dsw.getInstance(),
    'www.macys.com': Macys.getInstance(),
    'www.michaelkors.com': Michaelkors.getInstance(),
    'www.swarovski.com': Swarovski.getInstance(),
    'www.lasenza.com': Lasenza.getInstance(),
    'www.reebok.com': Reebok.getInstance()
}


@scraper.route('/scraper', methods=['POST'])
def scrap():
    url = json.loads(request.data)["link"]
    cache = redis_client.get(url)
    if cache:
        return jsonify(json.loads(cache))
    parse_obj = urlparse(url)
    web, response = Base, {}
    web = REQUEST_WEB.get(parse_obj.netloc, Base)
    response = web.product(url)
    try:
        response.update({
            'price': float(re.sub('[^.0-9]', '', response["price"]))
        })
        redis_client.set(url, json.dumps(response))
    except Exception as e:
        logging.error(e)
    return jsonify(response)

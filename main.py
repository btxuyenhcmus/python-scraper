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
import re


scraper = Blueprint('scraper', __name__)
CRAWLER = {
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


@scraper.route('/', methods=['POST'])
def get():
    url = json.loads(request.data)["link"]
    parse_obj = urlparse(url)
    web = CRAWLER.get(parse_obj.netloc, Base)
    response = web.product(url)
    try:
        response.update({
            'price': float(re.sub('[^.0-9]', '', response["price"]))
        })
    except Exception:
        pass
    return jsonify(response)

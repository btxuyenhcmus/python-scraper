from flask import Blueprint, json
from flask import request, jsonify
from walmart import Walmart
from walgreens import Walgreens


scraper = Blueprint('scraper', __name__)
web = Walmart.getInstance()


@scraper.route('/', methods=['POST'])
def get():
    url = json.loads(request.data)["link"]
    response = web.product(url)
    return jsonify(response)

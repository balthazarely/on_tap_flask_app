import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


beer = Blueprint('beer', 'beer', url_prefix="/beer/v1")
# will the "user" part just be a <userid>?


@beer.route('/', methods=["GET"])
def get_fav_beers():
    try:
        beer = [model_to_dict(beer) for beer in models.Beer.select()]
        return jsonify(data=beer, status={"code": 200, "message": "Success"})
    except models.DoesNotExisit:
        return jsonify(data={}, status={"code": 401, "message": "there was an error getting the resourse"})
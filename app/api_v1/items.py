from flask import jsonify, request
from . import api
from .. import graph
from ..decorators import json


@api.route('/items/<int:id>', methods=['GET'])
@json
def get_item(id):
    item = graph.contains.get(id)
    if item:
        return item.export_data()
    else:
        return {}, 404

@api.route('/items/<int:id>', methods=['PUT'])
@json
def edit_item(id):
    item = graph.contains.get(id)
    if not ('quantity' in request.json):
        return {}, 400
    if not item:
        return {}, 404
    else :
        item.quantity = request.json['quantity']
        item.save()
        return jsonify({})

@api.route('/items/<int:id>', methods=['DELETE'])
@json
def delete_item(id):
    if graph.contains.get(id):
        graph.contains.delete(id)
        return {}
    else:
        return {}, 404
from flask import  request
from . import api
from .. import graph
from ..decorators import json

@api.route('/products/', methods=['GET'])
@json
def get_products():
    if graph.products.get_all():
        return {'products': [product.get_url() for product in list(graph.products.get_all())]}
    else:
        return {}


@api.route('/products/<int:id>', methods=['GET'])
@json
def get_product(id):
    product = graph.products.get(id)
    if product and product.element_type == "Product":
        return product.export_data()
    else:
        return {}, 404


@api.route('/products/', methods=['POST'])
@json
def new_product():
    if 'name' in request.json:
        graph.products.create(name=request.json['name'])
        return {}, 201
    else:
        return {}, 400


@api.route('/products/<int:id>', methods=['PUT'])
@json
def edit_product(id):
    if not ('name' in request.json):
        return {}, 400
    product = graph.orders.get(id)
    if not product and product.element_type == "Product":
        return {}, 404
    else:
        product.name=request.json['name']
        product.save()
        return {}

from flask import  request
from . import api
from .. import graph
from ..decorators import json


#customer api
@api.route('/customers/', methods=['GET'])
@json
def get_customers():
    if graph.customers.get_all():
        return {'customers': [customer.get_url() for customer in list(graph.customers.get_all())]}
    else:
        return {}

@api.route('/customers/<int:id>', methods=['GET'])
@json
def get_customer(id):
    customer=graph.customers.get(id)
    if customer and customer.element_type == "Customer":
        return customer.export_data()
    else:
        return {'error': 'customer not found'}, 404


@api.route('/customers/', methods=['POST'])
@json
def new_customer():
    if 'name' in request.json:
        graph.customers.create(name=request.json['name'])
        return {}, 201
    else:
        return {}, 400


@api.route('/customers/<int:id>', methods=['PUT'])
@json
def edit_customer(id):
    customer=graph.customers.get(id)
    if not ('name' in request.json):
        return {}, 400
    if not customer and customer.element_type == "Customer":
        return {}, 404
    else:
        customer = graph.customers.get(id)
        customer.name=request.json['name']
        customer.save()
        return {}

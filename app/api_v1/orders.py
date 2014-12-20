from flask import  request
from . import api
from .. import graph
from ..decorators import json



#order api
@api.route('/orders/', methods=['GET'])
@json
def get_orders():
    if graph.orders.get_all():
        return ({'orders': [order.get_url() for order in
                                  list(graph.orders.get_all())]})
    else:
        return ({})

@api.route('/customers/<int:id>/orders/', methods=['GET'])
@json
def get_customer_orders(id):
    if graph.customers.get(id):
        customer=graph.customers.get(id);
        if customer.outV('ordered'):
            return {'orders': [order.get_url() for order in customer.outV('ordered')]}
        else:
            return ({})
    else:
        return ({}), 404
    ##



@api.route('/orders/<int:id>', methods=['GET'])
@json
def get_order(id):
    order = graph.orders.get(id)
    if  order and order.element_type == "Order":
        return order.export_data()
    else:
        return {}, 404

@api.route('/customers/<int:id>/orders/', methods=['POST'])
@json
def new_customer_order(id):
    customer=graph.customers.get(id)
    if not customer:
        return ({}), 404
    else:
        order = graph.orders.create()
        graph.ordered.create(customer,order)
        return ({}), 201


@api.route('/orders/<int:id>/items/', methods=['GET'])
@json
def get_order_items(id):
    order=graph.orders.get(id)
    if order:
        if order.outE('Contains'):
            return {'items': [item.get_url() for item in list(order.outE('Contains'))]}
        else:
            return {}
    else:
        return ({}), 404




@api.route('/orders/<int:id>', methods=['PUT'])
@json
def edit_order(id):
    order = graph.orders.get(id)
    if not ('name' in request.json):
        return ({}), 400
    if not (order):
        return ({}), 404
    else :
        order.name=request.json['created']
        order.save()
        return ({})

@api.route('/orders/<int:id>', methods=['DELETE'])
@json
def delete_order(id):
    if graph.orders.get(id):
        graph.orders.delete(id)
        return ({})
    else:
        return ({}), 404

@api.route('/orders/<int:id>/items/', methods=['POST'])
@json
def new_order_item(id):

    if not ('quantity' and 'product_id' in request.json):
        return {}, 400
    order = graph.orders.get(id)
    product = graph.products.get(request.json['product_id'])
    if not (order and product) and order.element_type == "Order" and product.element_type == "Product":
        return {}, 404
    else:
        item=graph.contains.create(order, product)
        item.quantity=request.json['quantity']
        item.save()
        return {}

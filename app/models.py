from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime
from bulbs.utils import current_datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from app import graph
from .exceptions import ValidationError
from .utils import split_url


class User(Node):
    element_type = "User"
    username = String(nullable=False,unique=True)
    password_hash = String(nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.eid}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return graph.users.get(data['id'])

    def get_node(self):
        return {
            'id': self.eid,
            'label': self.username
        }

class Customer(Node):
    element_type = "Customer"


    name = String(nullable=False)

    def get_url(self):
        return url_for('api.get_customer', id=self.eid, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name
        }

    def get_node(self):
        return {
            'id': self.eid,
            'label': self.name
        }

class Product(Node):
    element_type = "Product"
    label = "Product"

    name = String(nullable=False)

    def get_url(self):
        return url_for('api.get_product', id=self.eid, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name
        }
    def get_node(self):
        return {
            'id': self.eid,
            'label': self.name
        }

class Order(Node):
    element_type = "Order"
    label = "Order"
    created = DateTime(default=current_datetime, nullable=False)

    def get_url(self):
        return url_for('api.get_order', id=self.eid, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'date': self.created
        }

    def get_node(self):
        return {
            'id': self.eid,
            'label': self.created
        }




class Ordered(Relationship):
    label = "Ordered"

class Contains(Relationship):
    label = "Contains"
    quantity = Integer(nullable=True)
    def get_url(self):
        return url_for('api.get_item', id=self.eid, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'quantity': self.quantity
        }

    def get_edge(self):
        return {
            'from': self.inV(),
            'to': self.inV()
        }



graph.add_proxy("users", User)
graph.add_proxy("customers", Customer)
graph.add_proxy("products", Product)
graph.add_proxy("orders", Order)
graph.add_proxy("ordered", Ordered)
graph.add_proxy("contains", Contains)
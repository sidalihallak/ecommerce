from flask import  request
from . import api
from .. import graph
from ..decorators import json



#order api
@api.route('/network/', methods=['GET'])
@json
def get_nodes():
    if graph.vertices.get_all():
        return {
            'nodes': [node.get_node() for node in
                                  list(graph.vertices.get_all())],
            'edges':[{'from':graph.edges.get(edge.eid).outV().eid, 'to':graph.edges.get(edge.eid).inV().eid} for edge in
                         list(graph.edges.get_all())]
        }
    else:
        return {}


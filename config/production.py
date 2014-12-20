from app import graph
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
config = Config(NEO4J_URI, "james", "secret")
graph.config = config
DEBUG = False
SECRET_KEY = 'top-secret!'

from .algo import Algo
from .dummy import DummyAlgo

class Kmeans(DummyAlgo):
    """Todo: implement the acutal kmeans algo"""
    @property
    def name(self):
        return "Kmeans"

    @property
    def extra(self):
        return "Kmeans not implemented. Returning dummy algorithm."
    
    
import numpy as np
import networkx as nx
import osmnx as ox


class State:
    def __init__(self, drivers, riders):
        self.drivers = drivers
        self.riders = riders
        self.states = np.ndarray([2, 3])

    def get_network(self):
        pass

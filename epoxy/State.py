import numpy as np
import networkx as nx
import osmnx as ox

from Rider import Rider


class State:
    def __init__(self, drivers, riders, ride_data):
        self.drivers = drivers
        self.riders = riders
        self.states = np.ndarray([2, 3])
        self.set_drivers_random()
        self.ride_data = ride_data

    def set_drivers_random(self):
        for driver in self.drivers:
            driver.set_random_position()

    def get_new_riders(self, time):
        new_riders = []
        for value in self.ride_data:
            if value["pickup_time"] == time:
                new_riders.append(Rider(value["PULocationID"], value["DOLocationID"]))
        return new_riders

    def update_riders(self, time):
        updated_riders = []
        for rider in self.riders:
            flag = rider.update_rider()
            if flag:
                updated_riders.append(rider)
        updated_riders += self.get_new_riders(time)

    def get_network(self):
        pass

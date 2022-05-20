import numpy as np
import networkx as nx
import osmnx as ox

from Rider import Rider
from Driver import Driver


class StateGraph:
    def __init__(self, number_drivers, ride_data, current_time, graph):
        self.number_drivers = number_drivers
        self.drivers = self.set_drivers_random()
        self.time = current_time
        self.ride_data = ride_data
        self.riders = self.get_new_riders()
        self.state = [self.drivers, self.riders, self.time]
        self.graph = graph
        self.missed = 0
        self.action = 0

    def set_drivers_random(self):
        drivers = []
        for _ in range(self.number_drivers):
            drivers.append(Driver(1))
        return drivers

    def set_time(self, time):
        self.time = time

    def get_new_riders(self):
        new_riders = []
        for value in self.ride_data:
            if int(value["pickup_time"]) <= self.time + 100:
                new_riders.append(Rider(value["PULocationID"], value["DOLocationID"]))
        return new_riders

    def update_riders(self):
        updated_riders = []
        for rider in self.riders:
            flag = rider.update()
            if flag:
                updated_riders.append(rider)
            else:
                self.missed += rider.get_wait_time()
        updated_riders += self.get_new_riders()

    def evaluate_state(self):
        total = 0
        for rider in self.riders:
            total += rider.get_wait_time()
        return total + self.missed

    def perform_action(self, actions, time):
        self.time = time
        self.action = actions
        for driver in self.drivers:
            driver.give_rider_pos(self.any_riders_at_pos(driver.position))
        for i, action in enumerate(actions):
            self.drivers[i].use_action(action, self.graph)
        self.update_riders()
        return self

    def any_riders_at_pos(self, position):
        riders_list = []
        for rider in self.riders:
            if rider.start_position == position:
                riders_list.append(rider)
        return riders_list

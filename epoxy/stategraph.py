from collections.abc import MutableMapping

import numpy as np
import networkx as nx
import osmnx as ox
import pandas as pd
from gym import spaces
from gym.spaces import flatten, Dict

from epoxy.Rider import Rider
from epoxy.Driver import Driver


class StateGraph:
    def __init__(self, number_drivers, ride_data, current_time, graph):
        self.number_drivers = number_drivers
        self.drivers = []
        self.time = current_time
        self.ride_data = ride_data
        self.amount_of_riders = 0
        self.riders = []
        self.update_riders()
        self.state = [self.drivers, self.riders, self.time]
        self.graph = graph
        self.missed = 0
        self.actions = 0
        self.dropped_off_riders = []

    def set_drivers_random(self, nodes_list):
        self.drivers = []
        for i in range(self.number_drivers):
            self.drivers.append(Driver(1, nodes_list, i))
        return self.drivers

    def set_time(self, time):
        self.time = time

    def update_riders(self):
        updated_riders = []
        for rider in self.riders:
            flag = rider.update()
            if flag:
                updated_riders.append(rider)
            else:
                self.missed += rider.get_wait_time()
        self.riders = updated_riders
        counter = len(self.riders)
        for index, value in enumerate(self.ride_data[self.amount_of_riders:]):
            if int(value["pickup_time"]) <= self.time:
                self.riders.append(Rider(value["pickup_time"], counter, value["PULocationID"],
                                         value["DOLocationID"]))
                counter += 1
        self.amount_of_riders += counter

    def evaluate_state(self):
        total = 0
        for rider in self.riders:
            total += rider.get_wait_time()
        for driver in self.drivers:
            total += driver.get_wait_time()
        return -(total + self.missed)

    def remove_riders(self, riders):
        new_riders = []
        for rider in self.riders:
            for rider2 in riders:
                if not(rider == rider2):
                    new_riders.append(rider)
        self.riders = new_riders

    def perform_action(self, actions, time):
        self.time = time
        self.actions = actions
        for i, action in enumerate(self.actions[0]):
            if isinstance(action, bool) and action:
                driver_obj = self.drivers[i]
                pos = driver_obj.get_position()
                rider_pos = self.any_riders_at_pos(pos)
                driver_obj.use_action(action, self.graph, rider_pos)
            elif isinstance(action, bool) and not action:
                riders = self.drivers[i].use_action(action, self.graph)
                self.dropped_off_riders.append(riders)
                self.remove_riders(riders)
            else:
                self.drivers[i].use_action(action, self.graph)
        self.update_riders()
        return self

    def any_riders_at_pos(self, position):
        riders_list = []
        for rider in self.riders:
            if int(rider.start_position) == int(position):
                riders_list.append(rider)
        return riders_list

    def state_in_arrays(self):
        drivers_list = []
        for driver in self.drivers:
            drivers_list.append(driver.arrays())
        riders_list = []
        for rider in self.riders:
            riders_list.append(rider.arrays())
        return [drivers_list, riders_list]

    def to_dict(self):
        drivers_list = []
        for driver in self.drivers:
            drivers_list.append(driver.to_dict())
        riders_list = []
        for rider in self.riders:
            riders_list.append(rider.to_dict())
        output = {'driver': drivers_list, 'rider': riders_list}
        # value = pd.json_normalize(output, sep='.').to_dict(orient='records')
        return output

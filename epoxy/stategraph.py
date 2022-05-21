import numpy as np
import networkx as nx
import osmnx as ox

from Rider import Rider
from Driver import Driver


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

    def set_drivers_random(self, nodes_list):
        self.drivers = []
        for _ in range(self.number_drivers):
            self.drivers.append(Driver(1, nodes_list))
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
        counter = 0
        for index, value in enumerate(self.ride_data[self.amount_of_riders:]):
            if int(value["pickup_time"]) <= self.time:
                self.riders.append(Rider(value["pickup_time"], value["PULocationID"],
                                         value["DOLocationID"], index))
                counter += 1
        self.amount_of_riders += counter

    def evaluate_state(self):
        total = 0
        for rider in self.riders:
            total += rider.get_wait_time()
        return -(total + self.missed)

    def remove_riders(self, riders):
        new_riders = []
        for rider in self.riders:
            if rider not in riders:
                new_riders.append(rider)
        self.riders = new_riders

    def perform_action(self, actions, time):
        self.time = time
        self.actions = actions
        for driver in self.drivers:
            driver.give_rider_pos(self.any_riders_at_pos(driver.position))
        for i, action in enumerate(self.actions):
            if action:
                driver_obj = self.drivers[i]
                pos = driver_obj.get_position()
                driver_obj.use_action(action, self.graph, self.any_riders_at_pos(pos))
            elif not action:
                riders = self.drivers[i].use_action(action, self.graph)
                self.remove_riders(riders)
            else:
                self.drivers[i].use_action(action, self.graph)
        self.update_riders()
        return self

    def any_riders_at_pos(self, position):
        riders_list = []
        for rider in self.riders:
            if rider.start_position == position:
                riders_list.append(rider)
        return riders_list

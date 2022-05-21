import random

import networkx as nx

from Rider import Rider


class Driver:
    def __init__(self, capacity, possible_nodes):
        self.position = random.choice(possible_nodes)
        self.capacity = capacity
        self.riders = []
        self.on_route = False
        self.wait_time = 0
        self.current_time = 0
        self.picked_up_time = 0
        self.actual_time = 0
        self.available = True
        self.update_value = False
        self.riders_at_location = []

    def set_position(self, position):
        self.position = position

    def is_available(self):
        return self.available

    def move_car(self, which_node):
        self.position = which_node

    def give_rider_pos(self, riders):
        self.riders_at_location = riders

    def update(self):
        self.actual_time += 1
        # if len(self.riders) + self.riders_at_location[0].number_of_riders() < self.capacity:
        #     self.riders += self.riders_at_location
        if self.on_route:
            if self.current_time == self.actual_time:
                self.drop_riders()
            elif self.current_time == 0:
                self.current_time = self.riders[0]["pickup_time"] + self.actual_time
        else:
            self.wait_time += 1

    def drop_riders(self):
        temp_store = []
        get_rid_of = []
        for rider in self.riders:
            if rider.destination != self.position:
                temp_store.append(rider)
            else:
                get_rid_of.append(rider)
        self.riders = temp_store
        self.wait_time = 0
        self.available = True
        self.on_route = False
        return get_rid_of

    def get_position(self):
        return self.position

    def get_riders(self):
        return self.riders

    def is_on_route(self):
        return self.on_route

    def get_wait_time(self):
        return self.wait_time

    def navigate_to(self, target, graph):
        self.position = nx.shortest_path(graph, source=self.position, target=target)[1]
        self.on_route = False
        self.available = False

    def pick_up(self, riders_at_loc: [Rider]):
        length_riders = len(self.riders)
        i = 0
        while self.capacity < length_riders and i < len(riders_at_loc):
            if length_riders + len(riders_at_loc[i]) <= self.capacity:
                self.riders.append(riders_at_loc[i])
            i += 1

    def use_action(self, action, graph, riders_at_location=None):
        if riders_at_location is None:
            riders_at_location = []
        if action != 0:  # if not nothing action
            self.navigate_to(action, graph)
        elif action:  # pickup
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            self.pick_up(riders_at_location)
        else:  # drop_off
            return self.drop_riders()



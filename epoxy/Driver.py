import random

import networkx as nx


class Driver:
    def __init__(self, capacity):
        self.position = random.randint(2, 262)
        self.capacity = capacity
        self.riders = []
        self.on_route = False
        self.wait_time = 0
        self.current_time = 0
        self.picked_up_time = 0
        self.actual_time = 0
        self.available = True
        self.update_value = False
        self.riders_at_location = None

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
        if len(self.riders) + self.riders_at_location.number_of_riders() < self.capacity:
            self.riders += self.riders_at_location
        if self.on_route:
            if self.current_time == self.actual_time:
                self.drop_riders()
            elif self.current_time == 0:
                self.current_time = self.riders[0]["pickup_time"] + self.actual_time
        else:
            self.wait_time += 1

    def drop_riders(self):
        self.riders = []
        self.wait_time = 0
        self.available = True
        self.on_route = False

    def get_position(self):
        return self.position

    def get_riders(self):
        return self.riders

    def is_on_route(self):
        return self.on_route

    def get_wait_time(self):
        return self.wait_time

    def navigate_to(self, target, graph):
        self.position = nx.shortest_path(graph, source=self.position, target=target)[0]
        self.on_route = True
        self.available = False

    def use_action(self, action, graph):
        self.update()
        if action != 0:  # if not nothing action
            self.navigate_to(action, graph)

    def __str__(self):
        return str("hi")



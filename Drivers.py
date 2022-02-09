import random

from Node import Node


class Drivers:
    def __init__(self, capacity):
        self.position = []  # [[One node, Second node], Weight away from first node]
        self.capacity = capacity
        self.riders = []
        self.speed = 0.2

    def set_position(self, position):
        self.position = position

    def set_random_position(self, nodes: [Node]):
        nodes = []
        first_choice = random.choice(nodes)
        second_choice = first_choice.give_random_neighbour()[0]
        weight = first_choice.give_random_neighbour()[1]
        self.position = [[first_choice, second_choice], weight]

    def update_position(self):
        self.position[1] += self.speed
        distance = self.position[0][0].give_distance_from_neighbour(self.position[0][1])
        if self.position[1] == distance:
            current_position = self.position[0][1]
            next_position = self.get_next_node(current_position)
            weight = current_position.give_distance_from_neighbour(next_position)
            self.position = [[current_position, next_position], weight]

    def get_next_node(self, current_node: Node):
        neighbours_list = current_node.get_neighbours()
        return random.choice(neighbours_list)

    def get_position(self):
        return self.position

    def get_riders(self):
        return self.riders

    def __str__(self):
        return str("hi")

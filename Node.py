class Node:
    def __init__(self, index: int):
        self.index = index
        self.neighbours = []

    def give_neighbours(self,  neighbours: []):
        self.neighbours.append(neighbours)  # [[Node, Weight], [Node2, Weight2], ...]

    def give_distance_from_neighbour(self, neighbour):
        return self.neighbours.index(neighbour)[1]

    def get_neighbours(self):
        return [index[0] for index in self.neighbours]

    def __str__(self):
        return str(self.neighbours)

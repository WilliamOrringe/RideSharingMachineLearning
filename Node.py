class Node:
    def __init__(self, index: int):
        self.index = index
        self.neighbours = []

    def give_neighbours(self,  neighbours: []):
        self.neighbours.append(neighbours)  # [[Node, Weight], [Node2, Weight2], ...]

    def __str__(self):
        return str(self.neighbours)

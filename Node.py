class Node:
    def __init__(self, index: int, neighbours: [[]]):
        self.index = index
        self.neighbours = neighbours  # [[Node, Weight], [Node2, Weight2], ...]

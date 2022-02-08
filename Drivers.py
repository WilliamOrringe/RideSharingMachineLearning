class Drivers:
    def __init__(self, capacity):
        self.position = []  # [[One node, Second node], [Percentage of first node]]
        self.capacity = capacity
        self.riders = []

    def get_position(self):
        return self.position

    def get_riders(self):
        return self.riders

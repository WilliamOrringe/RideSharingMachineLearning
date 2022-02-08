class Drivers:
    def __init__(self, capacity):
        self.position = []  # [[One node, Second node], Weight away from first node]
        self.capacity = capacity
        self.riders = []
        self.speed = 0.2

    def set_position(self, position):
        self.position = position

    def update_position(self):
        self.position[1] += self.speed

    def get_position(self):
        return self.position

    def get_riders(self):
        return self.riders

    def __str__(self):
        return self.position

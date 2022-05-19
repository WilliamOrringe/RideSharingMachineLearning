class Driver:
    def __init__(self, capacity):
        self.position = self.set_random_position()
        self.capacity = capacity
        self.riders = []
        self.speed = 1

    def set_position(self, position):
        self.position = position

    def set_random_position(self):
        return 32


    def move_car(self, which_node):
        self.position = which_node

    def drop_riders(self):
        self.riders = []

    def get_position(self):
        return self.position

    def get_riders(self):
        return self.riders

    def __str__(self):
        return str("hi")



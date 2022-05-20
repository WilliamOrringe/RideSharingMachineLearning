class Driver:
    def __init__(self, capacity):
        self.position = self.set_random_position()
        self.capacity = capacity
        self.riders = []
        self.on_route = False
        self.wait_time = 0
        self.current_time = 0
        self.picked_up_time = 0
        self.actual_time = 0
        self.available = True
        self.update_value = False

    def set_position(self, position):
        self.position = position

    def set_random_position(self):
        return 32

    def is_available(self):
        return self.available

    def move_car(self, which_node):
        self.position = which_node

    def update(self):
        self.actual_time += 1
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

    def use_action(self, action):
        self.update()
        if action == 0:
            pass

    def __str__(self):
        return str("hi")



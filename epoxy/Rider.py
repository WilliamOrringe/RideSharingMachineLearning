class Rider:
    def __init__(self, start=10, destination=101):
        self.start_position = start  # which node
        self.number_of_riders = 1
        self.destination = destination  # Some area code
        self.wait_time = 0
        self.in_car = False
        self.bound = 10

    def update(self):
        if self.wait_time >= self.bound:
            return self.wait_time
        if not self.in_car:
            self.wait_time += 1 * self.number_of_riders

    def picked_up(self):
        self.in_car = True

    def get_wait_time(self):
        return self.wait_time

    def use_action(self, action):
        self.update()
        if action == 0:
            pass

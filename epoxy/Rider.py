class Rider:
    def __init__(self, start=10, destination=101):
        self.start_position = start  # which node
        self.numberOfRiders = 1
        self.destination = destination  # Some area code
        self.wait_time = 0
        self.in_car = False
        self.bound = 10

    def update_rider(self):
        if self.wait_time >= self.bound:
            return self.wait_time
        if not self.in_car:
            self.wait_time += 1 * self.numberOfRiders

    def picked_up(self):
        self.in_car = True

class Rider:
    def __init__(self):
        self.start_position = 10  # which node
        self.numberOfRiders = 1
        self.destination = 101  # Some area code
        self.wait_time = 0
        self.in_car = False

    def update_rider(self):
        if not self.in_car:
            self.wait_time += 1 * self.numberOfRiders

    def picked_up(self):
        self.in_car = True

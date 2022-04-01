from Driver import Driver
from Rider import Rider
from State import State

class Environment:
    def __init__(self):
        self.number_drivers = 5
        self.number_riders = 10
        self.drivers = [Driver() for _ in range(self.number_drivers)]
        self.riders = [Rider() for _ in range(self.number_riders)]
        self.state = State(self.drivers, self.riders)

    def state_space(self):
        pass

    def update_state_space(self):
        for riders in self.riders:
            riders.update_rider()


    def make_action(self, action):
        reward = 0
        state = self.drivers
        end_condition = False
        # Run simulation for One Frame
        return reward, state, end_condition

    def get_driver_action(self, driver):
        position = driver.get_position()


    def get_actions(self):
        return [self.drivers]

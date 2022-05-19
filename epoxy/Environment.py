from Driver import Driver
from Rider import Rider
from State import State
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
import random

from gym import spaces
import time


class Environment(gym.Env):
    def reset(self):
        self.__init__()

    def render(self, mode="human"):
        pass

    def step(self, action):
        pass

    def __init__(self):
        self.number_drivers = 5
        self.number_riders = 10
        self.drivers = [Driver(2) for _ in range(self.number_drivers)]
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

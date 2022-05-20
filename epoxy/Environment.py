from Driver import Driver
from Rider import Rider
from State import State
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
import csv
import random

from gym import spaces
import time


def get_ride_data():
    file = open('../data/cleandata/clean_data.csv', 'r')
    csv_reader = csv.DictReader(file)
    file_data = []
    for row in csv_reader:
        file_data.append(row)
    return file_data[:10]


class Environment(gym.Env):
    def __init__(self):
        super(Environment, self).__init__()
        self.number_drivers = 500
        self.number_riders = 10
        self.current_time = 0
        self.ride_data = get_ride_data()
        self.state = State(self.number_drivers, self.ride_data, self.current_time)
        self.action_space = spaces.Discrete(6, )
        # Define a 2-D observation space
        self.observation_shape = (600, 800, 3)
        self.observation_space = spaces.Discrete(6,)
        self.length_of_state = len(self.ride_data[0])
        self.new_obs_space = [i for i in range(self.length_of_state * 10)]

    def reset(self):
        self.__init__()
        return 0

    def render(self, **kwargs):
        pass

    def step(self, action):
        self.state = self.state.perform_action(action, self.current_time)
        self.current_time += 1
        reward = self.state.evaluate_state()
        info = "hi"
        return self.state, reward, info

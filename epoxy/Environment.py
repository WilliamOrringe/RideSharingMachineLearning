import networkx as nx
import pandas as pd
import numpy as np
from epoxy.Driver import Driver
# from State import State
import gym
import csv
from gym.spaces import Box, Dict, Discrete, MultiDiscrete

from epoxy.stategraph import StateGraph


def get_ride_data():
    file = open('../data/cleandata/clean_data2.csv', 'r')
    csv_reader = csv.DictReader(file)
    file_data = []
    for row in csv_reader:
        file_data.append(row)
    return file_data[:30]


def generate_graph():
    df = pd.read_csv('../data/cleandata/adjacent_zone2.csv')
    number_zones = 263
    G = nx.Graph()
    for j in range(number_zones):
        G.add_node(j)
    for i in range(len(df)):
        G.add_edge(df.at[i, 'zone1'], df.at[i, 'zone2'])
    return G


class Environment(gym.Env):
    def __init__(self, number_drivers=1):
        super(Environment, self).__init__()
        self.number_drivers = number_drivers
        self.current_time = 0
        self.ride_data = get_ride_data()
        # self.state = State(self.number_drivers, self.ride_data, self.current_time)
        graph_data = generate_graph()
        self.state = StateGraph(self.number_drivers, self.ride_data, self.current_time,
                                graph_data)
        node_list = self.find_nodes_with_paths()
        self.state.set_drivers_random(node_list)
        self.number_riders = len(self.ride_data)
        self.number_iterations = 100
        self.number_zones = 263
        self.action_space = Box(-2, self.number_zones, [1, number_drivers], dtype=int)
        driver = Dict(position=Discrete(self.number_zones + 3),
                      riders=Box(0, self.number_riders, [1, self.number_riders], dtype=int),
                      wait_time=Discrete(self.number_iterations))
        rider = Dict(rider_id=Discrete(self.number_iterations), start_pos=Discrete(self.number_zones),
                     start_time=Discrete(self.number_iterations), wait_time=Discrete(
                self.number_iterations),
                     destination=Discrete(self.number_zones), in_car=Discrete(1))
        self.observation_space = Dict(driver=driver, rider=rider)

    def reset(self):
        self.__init__()
        return self.state.to_dict()

    def render(self, **kwargs):
        print("------------------------")
        print("CURRENT TIME = ", self.current_time)
        for driver in self.state.drivers:
            print(driver)
        print("++++++++++++++++++++++++")
        for rider in self.state.riders:
            print(rider)
        print("------------------------")
        print("Reward = " + str(self.state.evaluate_state()))

    def step(self, action):
        self.state = self.state.perform_action(action, self.current_time)
        self.current_time += 1
        reward = self.state.evaluate_state()
        info = "hi"
        return self._get_obs(), reward, False, info

    def _get_obs(self):
        return self.state.to_dict()

    def generate_all_actions(self):
        drivers = self.state.drivers
        actions = []
        for driver in drivers:
            actions.append(self.generate_actions(driver))
        return actions

    def generate_actions(self, driver):
        return nx.descendants(self.state.graph, driver.get_position()) | {0} | {True} | {False}

    def find_nodes_with_paths(self):
        nodes_with_paths = []
        for j in range(len(self.state.graph.nodes)):
            driver = Driver(1, [j], j)
            value = self.generate_actions(driver)
            if len(tuple(value)) > 2:
                nodes_with_paths.append(j)
        return nodes_with_paths


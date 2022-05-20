import networkx as nx
import pandas as pd
from State import State
import gym
import csv
from gym import spaces

from epoxy.stategraph import StateGraph


def get_ride_data():
    file = open('../data/cleandata/clean_data.csv', 'r')
    csv_reader = csv.DictReader(file)
    file_data = []
    for row in csv_reader:
        file_data.append(row)
    return file_data[:1000]


def generate_graph():
    df = pd.read_csv('../data/cleandata/adjacent_zone.csv')
    G = nx.MultiDiGraph()
    for j in range(len(df)):
        G.add_node(j)
    for i in range(len(df)):
        G.add_edge(df.at[i, 'zone1'], df.at[i, 'zone2'])
    print(G)
    return G


class Environment(gym.Env):
    def __init__(self):
        super(Environment, self).__init__()
        self.number_drivers = 1
        self.current_time = 0
        self.ride_data = get_ride_data()
        # self.state = State(self.number_drivers, self.ride_data, self.current_time)
        self.state = StateGraph(self.number_drivers, self.ride_data, self.current_time,
                                generate_graph())
        self.action_space = spaces.Discrete(6, )
        # Actions = [[]]
        # For one Driver [two things either give a node to go to, doNothing]
        # Define a 2-D observation space
        self.observation_shape = (600, 800, 3)
        self.observation_space = spaces.Space(self.observation_shape)
        self.length_of_state = len(self.ride_data[0])
        self.new_obs_space = [i for i in range(self.length_of_state * 10)]

    def reset(self):
        self.__init__()
        return 0

    def render(self, **kwargs):
        for i, driver in enumerate(self.state.drivers):
            print("For Driver : " + str(i) + ", zone=" + str(driver.get_position()))
        print("------------------------")
        print("Reward = " + str(self.state.evaluate_state()))

    def step(self, action):
        self.state = self.state.perform_action(action, self.current_time)
        self.current_time += 1
        reward = self.state.evaluate_state()
        info = "hi"
        return self.state, reward, info

    def generate_all_actions(self):
        drivers = self.state.drivers
        actions = []
        for driver in drivers:
            actions.append(self.generate_actions(driver))
        return actions

    def generate_actions(self, driver):
        return nx.descendants(self.state.graph, driver.get_position()) | {0}



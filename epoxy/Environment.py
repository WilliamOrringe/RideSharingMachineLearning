import networkx as nx
import pandas as pd

from Driver import Driver
from State import State
import gym
import csv
from gym import spaces

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
        print("------------------------")
        print("CURRENT TIME = ", self.current_time)
        for i, driver in enumerate(self.state.drivers):
            print("Drivers : " + str(i) + ", zone=" + str(driver.get_position()))
        print("++++++++++++++++++++++++")
        for i, rider in enumerate(self.state.riders):
            print("Riders : " + str(rider.rider_id) + ", zone=" + str(rider.start_position) +
                  ", time = " + str(rider.start_time) + ", waiting for " +
                  str(rider.get_wait_time()) + ", end_zone=" + str(rider.destination))
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
        return nx.descendants(self.state.graph, driver.get_position()) | {0} | {True} | {False}

    def find_nodes_with_paths(self):
        nodes_with_paths = []
        for j in range(len(self.state.graph.nodes)):
            driver = Driver(1, [j])
            value = self.generate_actions(driver)
            if len(tuple(value)) > 2:
                nodes_with_paths.append(j)
        return nodes_with_paths


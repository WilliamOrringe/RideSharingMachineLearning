import random

from gym.spaces import MultiDiscrete, Box, Dict, Discrete
from gym.utils.env_checker import check_env
from gym.wrappers import FlattenObservation
from keras.layers import Flatten

from Driver import Driver
from epoxy.Environment import Environment


def setup():
    env = Environment()
    driver = Driver(1, [i for i in range(264)])
    driver.set_position(157)
    env.state.drivers = [driver]
    env.render()
    env.step([True])
    env.render()


def draw():
    number_drivers = 10
    time_steps = 30
    number_episodes = 10
    start_time = 0
    print("Loading Environment")
    env = Environment(number_drivers)
    env.current_time = 2
    print("Environment Loaded")
    env.render()
    print("Environment Rendered")
    for i in range(number_episodes):
        print("-+-+-+-+-+-+-+-+-+-+-")
        print("EPISODE : ", i+1)
        print("-+-+-+-+-+-+-+-+-+-+-")
        for j in range(start_time, time_steps + start_time):
            sub_val = env.generate_all_actions()
            sub_sub = []
            for k in range(number_drivers):
                sub_sub += [random.choice(tuple(sub_val[k]))]
            env.step(sub_sub)
            print("Actions used")
            print("----------------------")
            # env.render()


def goat():
    env = Environment(1)
    # check_env(env)
    driver = Driver(1, [i for i in range(264)], 1)
    driver.set_position(95)
    env.state.drivers = [driver]
    env.render()
    env.step([True])
    env.render()
    env.step([157])
    env.render()
    env.step([157])
    env.render()
    env.step([157])
    env.render()
    env.step([False])
    env.render()
    env.step([43])
    env.render()
    print(env.state.drivers[0])
    print(env.state.state_in_arrays())


def store():
    pass


if __name__ == "__main__":
    import numpy as np
    number_drivers = 10
    number_riders = 100
    number_iterations = 100
    number_zones = 263
    action_space = Box(-2, 263, [number_drivers, 1], dtype=int)
    # print(action_space)
    # print(action_space.sample())
    # print(action_space.shape)
    driver = Dict(position=Discrete(number_zones+3),
                  riders=Box(0, number_riders, [1, number_riders], dtype=int),
                  wait_time=Discrete(number_iterations))
    rider = Dict(rider_id=Discrete(number_iterations), start_pos=Discrete(number_zones),
                 start_time=Discrete(number_iterations), wait_time=Discrete(number_iterations),
                 destination=Discrete(number_zones), in_car=Discrete(1))
    observation_space = Dict(driver=driver, rider=rider)
    print(tel)
    print(observation_space)
    print(observation_space.shape)

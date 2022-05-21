import random

from Drivers import Drivers
from epoxy.Environment import Environment


def setup():
    env = Environment()


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


if __name__ == "__main__":
    draw()



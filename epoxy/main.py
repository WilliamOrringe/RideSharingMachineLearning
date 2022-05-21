import numpy as np
import gym
import random
# Initialize vehicles states X0
#  for t ∈ T do
# Get all ride requests at time t
# for Each ride request in time slot t do
# Choose a vehicle n to serve the request
# according to (7).
# Calculate the dispatch time using our model
#  in Section V-A.
# Update the state vector Ωt,n.
# end for
# Send the state vector Ωt to the agent.
# Get the best actions (dispatch orders) a_t from the agent.
# for all vehicles n ∈ at do
# Find the shortest path to every dispatch location for every vehicle n.
# Estimate the travel time using the model in Section V-A.
# Update δt,n, if needed, and generate the trajectory of vehicle n.
# end for
# Update the state vector Ωt+1.
# end for
from Environment import Environment
from gym.utils.env_checker import check_env


def generate_actions_random(env):
    actions = []
    all_actions = env.generate_all_actions()
    for action in all_actions:
        actions.append(random.choice(tuple(action)))
    return actions


def get_q_values(q, state: Environment, action=None):
    try:
        if action is None:
            return q[state, :]
        else:
            return q[state, action]
    except():
        return 0


def set_q_values(q, state, action, value):
    q[state, action] = value


def setup():
    env = Environment()
    # check_env(env)
    # env = gym.make("Taxi-v3")
    env.render()
    action_size = env.action_space.n
    print("Action size ", action_size)
    # state_size = env.observation_space.n
    state_size = env.observation_space.shape[0]
    print("State size ", state_size)
    q = []
    print(q)
    total_episodes = 2  # Total episodes
    max_steps = 30  # Max steps per episode
    gamma = 0.618  # Discounting rate
    epsilon = 1.0  # Exploration rate
    max_epsilon = 1.0  # Exploration probability at start
    min_epsilon = 0.01  # Minimum exploration probability
    decay_rate = 0.01  # Exponential decay rate for environment prob
    for episode in range(total_episodes):
        print(episode)
        # Reset the environment
        state = env.reset()
        for step in range(max_steps):  # step is current_time
            exp_exp_tradeoff = random.uniform(0, 1)
            if exp_exp_tradeoff > epsilon:
                action = np.argmax(get_q_values(q, state))
            else:
                # generate new action
                action = generate_actions_random(env)
            new_state, reward, info = env.step(action)
            secondary = reward + gamma * np.max(get_q_values(q, state))
            set_q_values(q, state, action, (get_q_values(q, state, action) *
                                            (secondary - get_q_values(q, state, action))))
            state = new_state
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        print(epsilon)


if __name__ == "__main__":
    setup()

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


def setup():
    env = gym.make("Taxi-v3")
    env.render()
    action_size = env.action_space.n
    print("Action size ", action_size)
    state_size = env.observation_space.n
    print("State size ", state_size)
    qtable = np.zeros((state_size, action_size))
    print(qtable)
    total_episodes = 50000  # Total episodes
    total_test_episodes = 100  # Total test episodes
    max_steps = 99  # Max steps per episode
    learning_rate = 0.7  # Learning rate
    gamma = 0.618  # Discounting rate
    # Exploration parameters
    epsilon = 1.0  # Exploration rate
    max_epsilon = 1.0  # Exploration probability at start
    min_epsilon = 0.01  # Minimum exploration probability
    decay_rate = 0.01  # Exponential decay rate for exploration prob
    # 2 For life or until learning is stopped
    for episode in range(total_episodes):
        # Reset the environment
        state = env.reset()
        step = 0
        done = False
        for step in range(max_steps):
            exp_exp_tradeoff = random.uniform(0, 1)
            if exp_exp_tradeoff > epsilon:
                action = np.argmax(qtable[state, :])
            else:
                action = env.action_space.sample()
            new_state, reward, done, info = env.step(action)
            qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma *
                                                                             np.max(
                                                                                 qtable[new_state,
                                                                                 :]) - qtable[
                                                                                 state, action])
            state = new_state
            if done:
                break
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)


if __name__ == "__main__":
    setup()

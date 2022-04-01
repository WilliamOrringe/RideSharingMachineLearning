import numpy as np
import gym
import random


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
            # 3. Choose an action a in the current world state (s)
            exp_exp_tradeoff = random.uniform(0, 1)

            if exp_exp_tradeoff > epsilon:
                action = np.argmax(qtable[state, :])

            # Else doing a random choice --> exploration
            else:
                action = env.action_space.sample()

            # Take the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done, info = env.step(action)

            # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
            qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma *
                                                                             np.max(
                                                                                 qtable[new_state,
                                                                                 :]) - qtable[
                                                                                 state, action])

            # Our new state is state
            state = new_state
            if done:
                break

        # Reduce epsilon (because we need less and less exploration)
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)


if __name__ == "__main__":
    setup()

import random
import numpy as np
import matplotlib
# setup matplotlib
matplotlib.use('TkAgg')
# import plot function
import matplotlib.pyplot as plt

class Arm:

    def __init__(self, random_step_variance=0.1):
        self.true_value = random.gauss(0,1)
        self.random_step_variance = random_step_variance

    def __str__(self):
        return str(self.true_value)

    def get_reward(self):
        return random.gauss(self.true_value, 1)

    def random_step(self):
        self.true_value += random.gauss(0, self.random_step_variance)

class Bandit:

    def __init__(self, k, stationary=True):
        self.k = k
        self.arms = [Arm() for i in range(k)]
        self.q_values = [0 for i in range(k)]
        self.count = [0 for i in range(k)]
        self.stationary = stationary

    def __str__(self):
        return 'true values: ' + ', '.join([str(arm) for arm in self.arms]) + \
        '\nq values: ' + ', '.join([str(q) for q in self.q_values]) + \
        '\ncount: ' + ', '.join([str(n) for n in self.count])

    def get_greedy_action(self):
        q_max = max(self.q_values)
        greedy_actions = [i for i, q in enumerate(self.q_values) if q == q_max]
        return greedy_actions[random.randint(0, len(greedy_actions)-1)]

    def get_random_action(self):
        return random.randint(0, k-1)

    # if alpha is supplied then recency weighted average is used
    # otherwise sample average is used
    def update(self, action, reward, alpha=None):
        # increment the action count
        self.count[action] += 1
        # updated arm if its non-stationary
        if not self.stationary:
            self.arms[action].random_step()
        # get q value to be updated
        q = self.q_values[action]
        # set alpha based on the action selection method
        if not alpha:
            alpha = 1.0 / self.count[action]
        # update q value for the selected action
        self.q_values[action] = q + alpha * (reward - q)

def run_bandit_sims(k, epsilon, alpha, stationary, num_bandits, num_steps):
    bandit_rewards = []
    for bandit_i in range(num_bandits):
        bandit = Bandit(k, stationary)
        step_rewards = []
        for step_i in range(num_steps):
            if random.random() > epsilon:
                action = bandit.get_greedy_action()
            else:
                action = bandit.get_random_action()
            reward = bandit.arms[action].get_reward()
            step_rewards.append(reward)
            bandit.update(action, reward, alpha)
        bandit_rewards.append(step_rewards)
    rewards = np.array(bandit_rewards)
    avg_rewards = list(np.mean(rewards, axis=0))
    return avg_rewards


# set parameters for simulations -----------------------------------------------

k = 10
epsilon = 0.1
alpha = None

stationary = True
num_bandits = 2000
num_steps = 1000

# plot something
# avg_rewards = run_bandit_sims(k, epsilon, alpha, stationary, num_bandits, num_steps)
# plt.plot(avg_rewards, color='b')

# figure something...
# avg_rewards = run_bandit_sims(k, 0, alpha, stationary, num_bandits, num_steps)
# plt.plot(avg_rewards, color='b')
# avg_rewards = run_bandit_sims(k, 0.1, alpha, stationary, num_bandits, num_steps)
# plt.plot(avg_rewards, color='g')
# avg_rewards = run_bandit_sims(k, 0.01, alpha, stationary, num_bandits, num_steps)
# plt.plot(avg_rewards, color='r')

#
# # exercise 2.3
stationary = True
avg_rewards = run_bandit_sims(k, epsilon, alpha, False, num_bandits, num_steps)
plt.plot(avg_rewards, color='g')
avg_rewards = run_bandit_sims(k, epsilon, 0.1, False, num_bandits, num_steps)
plt.plot(avg_rewards, color='r')


plt.show()

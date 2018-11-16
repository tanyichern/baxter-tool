import numpy as np
import gym
import simulation

env = gym.make('FetchTest-v1')
target = np.array([1.3, 0.75, -0.7])
while True:
    observed = env._get_obs()
    current_pos = observed['observation'][:3]
    deltas = target - current_pos
    action = np.array(deltas)
    action = np.append(action, [0.0])
    env.step(action)
    env.render()

import gym
import numpy as np
import matplotlib.pyplot as plt

def run_episode(env, parameters):
    observation = env.reset()
    totalreward = 0
    for _ in range(200):
        action = 0 if np.matmul(parameters,observation) < 0 else 1
        print(action)
        observation, reward, done, info = env.step(action)
        totalreward += reward
        if done:
            break
    return totalreward

def train(submit):
    env = gym.make('CartPole-v0')
    if submit:
        env.monitor.start('cartpole-experiments/', force=True)

    counter = 0
    bestparams = None
    bestreward = 0
    for _ in range(10000):
        counter += 1
        parameters = np.random.rand(4) * 2 - 1
        reward = run_episode(env,parameters)
        if reward > bestreward:
            bestreward = reward
            bestparams = parameters
            if reward == 200:
                break
        env.render()
    env.close()

    if submit:
        for _ in range(100):
            run_episode(env,bestparams)
        env.monitor.close()

    return counter

# train an agent to submit to openai gym
# train(submit=True)

# create graphs
results = []
for _ in range(1000):
    results.append(train(submit=False))

plt.hist(results,50,normed=1, facecolor='g', alpha=0.75)
plt.xlabel('Episodes required to reach 200')
plt.ylabel('Frequency')
plt.title('Histogram of Random Search')
plt.show()

print(np.sum(results) / 1000.0)

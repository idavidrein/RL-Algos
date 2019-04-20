import gym
import tensorflow as tf
import numpy as np

def explore(policy, env, steps, num_episodes, sess):
    trajectories = []
    rewards = []
    for i in range(num_episodes):
        observation = env.reset()
        trajectory = []
        reward_i = []
        for i in range(steps):
            action = sess.run([policy], observation)
            trajectory.append((observation, action))
            observation, reward, done, info = env.step(action)
            reward_i.append(reward)
            if done:
                print("Episode over after {0} timesteps".format(i+1))
                break
        trajectories.append(trajectory)
        rewards.append(reward_i)
        
    return trajectories, rewards

def compute_grad(policy, rewards, trajectories, sess):
    gradient = 0

    return gradient

def mlp(observation, seed, dims):
    obs_dim, hidden_units, action_dim = dims
    W1 = tf.Variable(tf.zeros([obs_dim, hidden_units]))
    W2 = tf.Variable(tf.zeros([hidden_units, action_dim]))
    b1 = tf.Variable(tf.zeros([hidden_units]))
    b2 = tf.Variable(tf.zeros([action_dim]))
    params = (W1, W2, b1, b2)
    layer_1 = tf.nn.relu(tf.add(tf.matmul(observation, W1), b1))
    layer_out = tf.nn.softmax(tf.add(tf.matmul(layer_1, W2)))
    log_out = tf.math.log(layer_out)
    return layer_out, log_out, params

def run(epochs = 5, learning_rate = .01, seed = 1, steps = 20, num_episodes = 100, environment = 'CartPole-v0'):
    env = gym.make(environment)
    action_dim = env.action_space.n
    obs_dim = env.observation_space.n
    hidden_units = 10
    dims = (env.observation_space.n, hidden_units, env.action_space.n)

    observation = tf.placeholder(tf.float32, [1, dims])
    policy, log_policy, params = mlp(observation, seed, (obs_dim, hidden_units, action_dim))

    with tf.Session() as sess:
	    for i in range(epochs):
	        trajectories, rewards = explore(policy, env, steps, num_episodes, sess)
	        grad = compute_grad(policy, rewards, trajectories, sess)
	        policy = tf.add(policy, learning_rate * grad)
    
    print("Done!")
    
    env.close()

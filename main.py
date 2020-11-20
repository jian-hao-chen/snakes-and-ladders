# -*- coding: utf-8 -*-
"""A `Snakes and Ladders` game for Reinforcement Learning algorithms.

Created on: 2020/11/06 17:29

An assignment for Reinforcement Learning Course of NTNU.
"""
import argparse
import time

from agent import Agent
from env import SnakesAndLadders

# Command line interface
parser = argparse.ArgumentParser()
parser.add_argument("-v",
                    "--version",
                    choices=['v0', 'v1', 'v2'],
                    required=True,
                    help="select the version of game.")
parser.add_argument("-s",
                    "--size",
                    choices=['small', 'medium', 'large'],
                    required=True,
                    help="select the size of game board.")
parser.add_argument("-i",
                    "--interval",
                    type=float,
                    default=0.5,
                    help=("the interval time of each round." +
                          " (default: 0.5 sec)"))
parser.add_argument("-E",
                    "--episode",
                    type=int,
                    default=10,
                    help="how many times to run.")
parser.add_argument("-r",
                    "--random",
                    type=int,
                    default=0,
                    help="how many random dice. (default: 0)")
parser.add_argument("-V",
                    "--visualize",
                    action="store_true",
                    help="set to display the training process.")
parser.add_argument("-a",
                    "--alpha",
                    type=float,
                    default=0.1,
                    help="learning rate. (default: 0.1)")
parser.add_argument("-y",
                    "--gamma",
                    type=float,
                    default=0.9,
                    help="decay rate. (default: 0.9)")
parser.add_argument("-e",
                    "--epsilon",
                    type=float,
                    default=0.1,
                    help="epsilon used in `eps-greedy`. (default: 0.2)")
parser.add_argument("-l",
                    "--lambda",
                    type=float,
                    default=0.9,
                    dest="Lambda",
                    help="lambda used in `TD(lambda)`. (default: 0.9)")
parser.add_argument("-q",
                    "--q",
                    action="store_true",
                    help="Use Q-Learning as training policy.")
args = parser.parse_args()
VERSION = args.version
SIZE = args.size
EPISODES = args.episode
INTERVAL = args.interval
NUM_RAND_DICE = args.random
VISAULIZE = args.visualize
ALPHA = args.alpha
GAMMA = args.gamma
EPSILON = args.epsilon
LAMBDA = args.Lambda
Q_LEARN = args.q


def std_temp_diff(env, agent):
    history = np.zeros(EPISODES)
    for ep in range(EPISODES):
        last_state = 0
        while env.board.viewer.isopen:
            # Chooses the action with value table.
            if np.random.rand() < EPSILON:
                action = agent.sample()
            else:
                action = agent.seek(last_state)
            observation, reward, done, info = env.step(action)
            # If encounter 'ladder' or 'snake', info stored the state before
            # enter the aisle.
            if info is not None:
                cur_state = info
            else:
                cur_state = observation
            # Updates eligibility by observation.
            agent.eligibility[cur_state] += 1
            # Computes TD error.
            delta = (GAMMA * agent.value_table[cur_state] + reward -
                     agent.value_table[last_state])
            # Updates the value table of agent.
            agent.value_table += ALPHA * delta * agent.eligibility
            # Updates the eligibility of agent.
            agent.eligibility *= GAMMA * LAMBDA
            # Updates last state.
            last_state = cur_state

            if VISAULIZE:
                env.render(observation, info, agent.value_table[1:])
            time.sleep(INTERVAL)
            if done:
                print(f"Episode {ep+ 1} finished. Total steps: {env.steps}.")
                history[ep] = env.steps
                env.reset()
                break
    return history


def q_learn(env, agent):
    history = np.zeros(EPISODES)
    for ep in range(EPISODES):
        last_state = 0
        while env.board.viewer.isopen:
            # Chooses the action with value table.
            if np.random.rand() < EPSILON:
                action = agent.sample()
            else:
                action = agent.seek(last_state)
            observation, reward, done, info = env.step(action)
            # If encounter 'ladder' or 'snake', info stored the state before
            # enter the aisle.
            if info is not None:
                cur_state = info
            else:
                cur_state = observation
            # Computes TD error.
            delta = (reward + GAMMA * agent.q_table[cur_state].max() -
                     agent.q_table[last_state].max())
            # Updates Q table.
            agent.q_table[cur_state][
                agent.q_table[cur_state].argmax()] += ALPHA * delta
            # Updates last state.
            last_state = cur_state

            if VISAULIZE:
                env.render(observation, info, agent.value_table[1:])
            time.sleep(INTERVAL)
            if done:
                print(f"Episode {ep+ 1} finished. Total steps: {env.steps}.")
                history[ep] = env.steps
                env.reset()
                break
    return history


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    # Initializes game environment and agent.
    game = SnakesAndLadders(VERSION, SIZE)
    agent = Agent(VERSION, game.goal, NUM_RAND_DICE, Q_LEARN)

    if Q_LEARN:
        history = q_learn(game, agent)
    else:
        history = std_temp_diff(game, agent)

    fig = plt.figure(dpi=144)
    ax = fig.add_subplot(1, 1, 1)
    x = [x + 1 for x in range(EPISODES)]
    ax.plot(x, history)
    ax.set_ylim(0, 100)
    ax.set_title('Steps per episode')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Steps')
    plt.savefig(f"img/{VERSION}_{SIZE}_{LAMBDA}.png")
    plt.show()

    game.close()
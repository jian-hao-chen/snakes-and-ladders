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
parser.add_argument("-e",
                    "--episode",
                    type=int,
                    default=10,
                    help="how many times to run.")
args = parser.parse_args()
VERSION = args.version
SIZE = args.size
EPISODES = args.episode
INTERVAL = args.interval


def std_temp_diff(env, agent, alpha, gamma, Lambda):
    for ep in range(EPISODES):
        last_state = 0
        while env.board.viewer.isopen:
            # Chooses the action to take by checking value table.
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
            delta = (gamma * agent.value_table[cur_state] + reward -
                     agent.value_table[last_state])
            # Updates the value table of agent.
            agent.value_table += alpha * delta * agent.eligibility
            # Updates the eligibility of agent.
            agent.eligibility *= gamma * Lambda
            # Updates last state.
            last_state = cur_state

            env.render(observation, info, agent.value_table[1:])
            time.sleep(INTERVAL)
            if done:
                print(f"Episode {ep+ 1} finished. Total steps: {env.steps}.")
                env.reset()
                break


if __name__ == "__main__":
    import numpy as np
    # Initializes game environment and agent.
    game = SnakesAndLadders(VERSION, SIZE)
    agent = Agent(VERSION, game.goal)

    if VERSION == 'v0':
        std_temp_diff(game, agent, 0.1, 0.9, 0.9)

    game.close()
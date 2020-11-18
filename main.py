# -*- coding: utf-8 -*-
"""A `Snakes and Ladders` game for Reinforcement Learning algorithms.

Created on: 2020/11/06 17:29

An assignment for Reinforcement Learning Course of NTNU.
"""
import argparse
import time

from agent import Agent
from env import SnakesAndLadders

if __name__ == "__main__":
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
    args = parser.parse_args()

    # Initializes game environment and agent.
    game = SnakesAndLadders(args.version, args.size)
    agent = Agent(args.version)
    episode = 0
    while game.board.viewer.isopen:
        observation, reward, done, info = game.step(agent.act())
        game.render(observation, info)
        time.sleep(args.interval)
        if done:
            episode += 1
            print(f'Episode {episode} finished. Total steps: {game.steps}.')
            game.reset()

    game.close()
# -*- coding: utf-8 -*-
"""Game environments for Reinforcement Learning algorithms.

Created on: 2020/11/08 16:53

Contents
"""
import numpy as np
import gym

import view


class SnakesAndLadders(gym.Env):
    """Creates a virtual `Snakes and Ladders` board game environment.
    """
    def __init__(self, version, size):
        self.ver = version
        if size not in ['small', 'medium', 'large']:
            print(f'Not supported size: "{size}", using "small".')
            size = 'small'
        self.cols = 10
        if size == 'small':
            self.rows = 10
            self.grid_size = 60
        elif size == 'medium':
            self.rows = 20
            self.grid_size = 45
        elif size == 'large':
            self.rows = 30
            self.grid_size = 35

        self.goal = self.rows * self.cols
        # The 'Ladders' and 'Snakes'.
        self.aisles = get_aisles(size)
        # The number of steps elapsed until the game over.
        self.steps = 0
        # The state of game, which means the number of the current grid.
        self.state = 0

        env_args = (self.cols, self.rows, self.grid_size, self.aisles)
        self.board = view.Board(env_args)

    def step(self, action):
        self.state += action
        reward = 0
        # If pass through the goal by the action, go backwards.
        if self.state > self.goal:
            self.state = self.state - (self.state - self.goal)

        # If encounter 'ladder' or 'snake', store the previous state in `info`.
        if self.state in self.aisles:
            info = self.state
            self.state = self.aisles[self.state]
            # If encounter 'ladder'
            if self.state > info:
                reward += 10 + (self.state - info)
            else:
                reward += -10 + (self.state - info)
        else:
            reward += -1
            info = None

        # If reach the goal, give more reward and finish this episode.
        if self.state == self.goal:
            reward += 100
            done = True
        else:
            done = False

        self.steps += 1
        observation = self.state
        return (observation, reward, done, info)

    def reset(self):
        self.state = 0
        self.steps = 0
        return

    def render(self, observation, info, value):
        return self.board.render(observation, info, value)

    def close(self):
        return self.board.close()


def get_aisles(size):
    aisles = {
        1: 38,
        4: 14,
        9: 31,
        17: 7,
        21: 42,
        28: 84,
        51: 67,
        54: 34,
        62: 19,
        64: 60,
        71: 91,
        80: 100,
        87: 24,
        93: 73,
        95: 75,
        98: 79
    }
    if size == 'small':
        return aisles
    elif size == 'medium':
        org_dict = aisles.copy()
        for key, value in org_dict.items():
            aisles[key + 100] = value + 100
        return aisles
    elif size == 'large':
        org_dict = aisles.copy()
        for key, value in org_dict.items():
            aisles[key + 100] = value + 100
            aisles[key + 200] = value + 200
        return aisles
    else:
        return aisles
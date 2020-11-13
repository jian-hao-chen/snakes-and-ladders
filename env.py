# -*- coding: utf-8 -*-
"""Game environments for Reinforcement Learning algorithms.

Created on: 2020/11/08 16:53

Contents
"""
import gym

import view


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
        for key, value in aisles.items():
            aisles[key + 100] = value + 100
        return aisles
    elif size == 'large':
        for key, value in aisles.items():
            aisles[key + 100] = value + 100
            aisles[key + 200] = value + 200
        return aisles
    else:
        return aisles


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
        self.aisles = get_aisles(size)

        env_args = (self.cols, self.rows, self.grid_size, self.aisles)
        self.viewer = view.Board(env_args)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        pass


if __name__ == "__main__":
    pass

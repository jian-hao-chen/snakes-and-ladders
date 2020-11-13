# -*- coding: utf-8 -*-
"""Game environments for Reinforcement Learning algorithms.

Created on: 2020/11/08 16:53

Contents
"""
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

        env_args = (self.cols, self.rows, self.grid_size)
        self.viewer = view.Board(env_args)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        pass


if __name__ == "__main__":
    pass

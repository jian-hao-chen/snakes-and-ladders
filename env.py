# -*- coding: utf-8 -*-
"""Game environments for Reinforcement Learning algorithms.

Created on: 2020/11/08 16:53

Contents
"""
import gym


class SnakesAndLadders(gym.Env):
    """Creates a virtual `Snakes and Ladders` board game environment.
    """
    def __init__(self, version):
        pass

    def _step(self, action):
        pass

    def _reset(self):
        pass


if __name__ == "__main__":
    from gym.envs.classic_control import rendering
    viewer = rendering.Viewer(800, 600)
    
    while True:
        viewer.render()
        if viewer.window_closed_by_user():
            break
    
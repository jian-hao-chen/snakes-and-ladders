# -*- coding: utf-8 -*-
"""Game agents for playing the game. In other words, it means how to roll the
dice and what points will the dice have.

Created on: 2020/11/18 21:53

Contents
"""
import numpy as np


class Agent(object):
    """Creates a virtual agent for interacting with the environment.
    """
    def __init__(self, version):
        if version == 'v0':
            # Generates a dictionary that map 0 ~ 5 to 1 ~ 6.
            self.action_space = dict((i, i + 1) for i in range(6))
            # The action of this agent.
            self.act = self.sample_v0
        elif version == 'v1':
            pass
        elif version == 'v2':
            pass
        else:
            raise ValueError(f'Unknown argument: {version}.')

    def sample_v0(self):
        n = len(self.action_space)
        choice = np.random.randint(n)
        return self.action_space[choice]
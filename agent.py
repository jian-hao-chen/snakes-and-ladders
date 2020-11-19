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
    def __init__(self, version, goal):
        if version == 'v0':
            # Generates a dictionary that map 0 ~ 5 to 1 ~ 6.
            self.action_space = dict((i, i + 1) for i in range(6))
            # The states start from 1 to goal
            self.value_table = np.zeros(goal + 1)
            self.eligibility = np.zeros(goal + 1)
        elif version == 'v1':
            pass
        elif version == 'v2':
            pass
        else:
            raise ValueError(f'Unknown argument: {version}.')

    def seek(self, state):
        acts = self.action_space
        # Finds all probable states by action space
        prob_states = np.array(list(acts.values()))
        prob_states += state
        candidate = self.value_table[prob_states]
        if candidate.all() == 0:
            return self.sample()
        else:
            return acts[np.argmax(candidate)]

    def sample(self):
        n = len(self.action_space)
        choice = np.random.randint(n)
        return self.action_space[choice]
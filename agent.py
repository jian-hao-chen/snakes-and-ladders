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
    def __init__(self, version, goal, num_rand_dice, q_learn):
        self.q_learn = q_learn
        if version == 'v0':
            # Generates a dictionary that map 0 ~ 5 to 1 ~ 6.
            self.action_space = dict((i, i + 1) for i in range(6))
            # The states start from 1 to goal
        elif version == 'v1':
            # 2 fixed dice, [1, 1, 3, 3, 5, 5] and [2, 2, 4, 4, 6, 6]
            if num_rand_dice == 0:
                odd_die = {0: 1, 1: 1, 2: 3, 3: 3, 4: 5, 5: 5}
                even_die = {0: 2, 1: 2, 2: 4, 3: 4, 4: 6, 5: 6}
                self.action_space = [odd_die, even_die]
            # Generates some random dice.
            else:
                self.action_space = []
                for _ in range(num_rand_dice):
                    self.action_space.append(
                        dict((i, np.random.randint(6) + 1) for i in range(6)))
        elif version == 'v2':
            pass
        else:
            raise ValueError(f'Unknown argument: {version}.')

        self.value_table = np.zeros(goal + 1)
        self.eligibility = np.zeros(goal + 1)
        if self.q_learn:
            self.q_table = np.zeros((goal + 1, len(self.action_space)))
        self.goal = goal

    def seek(self, state):
        acts = self.action_space
        # For v0, a normal die.
        if type(acts) == dict:
            # Finds all probable states by action space
            prob_states = np.array(list(acts.values())) + state
            prob_states = prob_states[prob_states <= self.goal]

            candidate = self.value_table[prob_states]
            if candidate.all() == 0:
                return self.sample()
            else:
                return acts[np.argmax(candidate)]
        # For v1 or v2, multiple dice.
        elif type(acts) == list:
            n_choice = len(acts)
            expectation = np.zeros(n_choice)
            # Computes expectation of each choice.
            for i in range(n_choice):
                prob_states = np.array(list(acts[i].values())) + state
                prob_states = prob_states[prob_states <= self.goal]
                if len(prob_states) > 0:
                    if self.q_learn:
                        expectation[i] += (self.q_table[prob_states, i].sum() /
                                           len(prob_states))
                    else:
                        expectation[i] += (
                            self.value_table[prob_states].sum() /
                            len(prob_states))
                else:
                    expectation[i] += 0
            # Finds the action (dice) which has max expectation.
            choice = np.argmax(expectation)
            if expectation.all() == 0:
                return self.sample()
            else:
                return acts[choice][np.random.randint(6)]

    def sample(self):
        # Single die sampling.
        if type(self.action_space) == dict:
            n = len(self.action_space)
            choice = np.random.randint(n)
            return self.action_space[choice]
        # Multiple dice sampling.
        elif type(self.action_space) == list:
            n_dice = len(self.action_space)
            rand_dice = np.random.randint(n_dice)
            n = len(self.action_space[rand_dice])
            choice = np.random.randint(n)
            return self.action_space[rand_dice][choice]
        else:
            raise TypeError(f'Unknown action space: {type(self.action_space)}')
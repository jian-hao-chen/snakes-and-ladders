# -*- coding: utf-8 -*-
"""Visualization of `Snakes and Ladders` environment.

Created on: 2020/11/09 15:49

Contents
"""
from gym.envs.classic_control import rendering

OFFSET = 10


class Board(object):
    """A sample game board taken from ISLCollective.
    """
    def __init__(self, size):
        if size not in ['small', 'medium', 'large']:
            print(f'Not supported size: "{size}", using "small".')
            size = 'small'

        self.cols = 10
        if size == 'small':
            self.rows = 10
            self.grid_size = 60
        elif size == 'medium':
            self.rows = 20
            self.grid_size = 50
        elif size == 'large':
            self.rows = 30
            self.grid_size = 35
        self.viewer = rendering.Viewer(self.cols * self.grid_size + OFFSET * 2,
                                       self.rows * self.grid_size + OFFSET * 2)
        # The background only need to be drawn once.
        self.draw_background()

    def draw_background(self):
        size = self.grid_size
        for x in range(self.cols):
            for y in range(self.rows):
                # Calculates the coordinates of each grid.
                v = [((x) * size + OFFSET, (y) * size + OFFSET),
                     ((x + 1) * size + OFFSET, (y) * size + OFFSET),
                     ((x + 1) * size + OFFSET, (y + 1) * size + OFFSET),
                     ((x) * size + OFFSET, (y + 1) * size + OFFSET)]
                grid = rendering.make_polygon(v, False)
                self.viewer.add_geom(grid)

    def render(self):
        return self.viewer.render()

    def close(self):
        return self.viewer.close()


if __name__ == "__main__":
    b = Board('large')
    while b.viewer.isopen:
        b.render()
    b.close()
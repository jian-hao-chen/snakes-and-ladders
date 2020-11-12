# -*- coding: utf-8 -*-
"""Visualization of `Snakes and Ladders` environment.

Created on: 2020/11/09 15:49

Contents
"""
import pyglet
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
            self.grid_size = 45
        elif size == 'large':
            self.rows = 30
            self.grid_size = 35

        # Creates a canvas with given size.
        self.viewer = rendering.Viewer(self.cols * self.grid_size + OFFSET * 2,
                                       self.rows * self.grid_size + OFFSET * 2)
        # Background flag for checking whether the background is drawn.
        self.background = None

    def draw_background(self):
        size = self.grid_size
        # Draws grids and numbers.
        for y in range(self.rows):
            for x in range(self.cols):
                # Calculates the coordinates of each grid.
                v = [((x) * size + OFFSET, (y) * size + OFFSET),
                     ((x + 1) * size + OFFSET, (y) * size + OFFSET),
                     ((x + 1) * size + OFFSET, (y + 1) * size + OFFSET),
                     ((x) * size + OFFSET, (y + 1) * size + OFFSET)]
                grid = rendering.make_polygon(v, False)
                self.viewer.add_geom(grid)

                # Claculates number.
                # if the number of the grid is in even rows. (starts from 0)
                if y % 2 == 0:
                    num = 1 + self.cols * y + x
                else:
                    num = 1 + self.cols * y + ((self.cols - 1) - x)
                # Top-left point of the grid.
                anchor = v[-1]
                num_text = Text(text=str(num),
                                font_size=size / 4,
                                x=anchor[0],
                                y=anchor[1])
                self.viewer.add_geom(num_text)
        return True

    def render(self):
        if self.background is None:
            self.background = self.draw_background()

        return self.viewer.render()

    def close(self):
        return self.viewer.close()


class Text(object):
    """Packages `pyglet.text.Label` class for openAI `gym` rendering process.
    """
    
    def __init__(self, text, font_size, x, y):
        self.label = pyglet.text.Label(text=text,
                                       font_size=font_size,
                                       x=x,
                                       y=y,
                                       anchor_x="left",
                                       anchor_y="top",
                                       color=(0, 0, 0, 255))

    def render(self):
        return self.label.draw()


if __name__ == "__main__":
    b = Board('medium')
    while b.viewer.isopen:
        b.render()

    b.close()
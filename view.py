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
    def __init__(self, env_args):
        self.cols, self.rows, self.grid_size, self.aisles = env_args

        # Creates a canvas with given size.
        self.viewer = rendering.Viewer(self.cols * self.grid_size + OFFSET * 2,
                                       self.rows * self.grid_size + OFFSET * 2)
        # A flag for checking whether the background is drawn.
        self.flag_bg = None
        # A flag for checking whether the aisles (ladder and snake) is drawn.
        self.flag_aisle = None

    def get_coordinate(self, num_of_grid):
        """Returns the coordinate by the number of given grid.
        """
        row = (num_of_grid - 1) // self.cols
        col = (num_of_grid - 1) % self.cols
        # If the number of the grid is in odd rows. (starts from 0)
        if row % 2 == 1:
            col = (self.cols - 1) - col
        # Computes the bottom-left corner coordinate of the relative grid.
        x = col * self.grid_size + OFFSET
        y = row * self.grid_size + OFFSET
        return (x, y)

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
                # If the number of the grid is in even rows. (starts from 0)
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

    def draw_aisles(self):
        size = self.grid_size
        for key, value in self.aisles.items():
            if key < value:
                select = 'Ladder'
            else:
                select = 'Snake'

            start_x, start_y = self.get_coordinate(key)
            # To make the aisles start from the central of a grid.
            start_x = start_x + size / 2
            start_y = start_y + size / 2

            end_x, end_y = self.get_coordinate(value)
            # To make the aisles end to the central of a grid.
            end_x = end_x + size / 2
            end_y = end_y + size / 2

            aisle = Aisle(select, (start_x, start_y), (end_x, end_y))
            self.viewer.add_geom(aisle)
        return True

    def render(self):
        if self.flag_bg is None:
            self.flag_bg = self.draw_background()
        if self.flag_aisle is None:
            self.flag_aisle = self.draw_aisles()

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


class Aisle(object):
    """Packages `rendering.Viewer.Line` class with some custom attributes.
    """
    def __init__(self, select, start, end):
        # The `glLineWidth` is not supported for unknown reason.
        # The compromise is drawing two lines that closing to each other.
        x1, y1 = start
        x2, y2 = end
        self.lines = []
        self.lines.append(rendering.Line(start, end))
        self.lines.append(rendering.Line((x1 + 1, y1), (x2 + 1, y2)))
        if select == 'Ladder':
            for line in self.lines:
                line.set_color(0, 0, 255)
        elif select == 'Snake':
            for line in self.lines:
                line.set_color(255, 0, 0)
                line.add_attr(rendering.LineStyle(0x00FF))
        else:
            raise ValueError('select only supports "Ladder" or "Snake".')

    def render(self):
        for line in self.lines:
            line.render()
        return

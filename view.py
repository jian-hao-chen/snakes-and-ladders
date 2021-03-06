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
        # Computes the centroid coordinate of the relative grid.
        x = col * self.grid_size + OFFSET + self.grid_size / 2
        y = row * self.grid_size + OFFSET + self.grid_size / 2
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
        for key, value in self.aisles.items():
            if key < value:
                select = 'Ladder'
            else:
                select = 'Snake'
            start_x, start_y = self.get_coordinate(key)
            end_x, end_y = self.get_coordinate(value)
            aisle = Aisle(select, (start_x, start_y), (end_x, end_y))
            self.viewer.add_geom(aisle)

        return True

    def render(self, state, info, value=None):
        if self.flag_bg is None:
            self.flag_bg = self.draw_background()
        if self.flag_aisle is None:
            self.flag_aisle = self.draw_aisles()

        # Draws the piece to represent the current state.
        radius = self.grid_size * 0.25
        coord = self.get_coordinate(state)
        piece = rendering.make_circle(radius)
        # Don't know why the `set_color()` method of circle requires values
        # between 0 and 1.
        piece.set_color(139 / 255, 69 / 255, 19 / 255)
        piece.add_attr(rendering.Transform(coord))
        self.viewer.add_onetime(piece)

        # If the piece pass through the 'ladder' or 'snake'.
        if info is not None:
            last_coord = self.get_coordinate(info)
            last_piece = rendering.make_circle(radius, filled=False)
            last_piece.set_color(94 / 255, 38 / 255, 18 / 255)
            last_piece.add_attr(rendering.Transform(last_coord))
            self.viewer.add_onetime(last_piece)

        if value is not None:
            for i, v in enumerate(value):
                x, y = self.get_coordinate(i + 1)
                v_str = Text(text=f"{v:.2f}",
                             font_size=self.grid_size / 5,
                             x=x,
                             y=y,
                             anchor_x="center",
                             anchor_y="center")
                self.viewer.add_onetime(v_str)

        return self.viewer.render()

    def close(self):
        return self.viewer.close()


class Text(object):
    """Packages `pyglet.text.Label` class for openAI `gym` rendering process.
    """
    def __init__(self,
                 text,
                 font_size,
                 x,
                 y,
                 anchor_x="left",
                 anchor_y="top",
                 color=(0, 0, 0, 255)):
        self.label = pyglet.text.Label(text=text,
                                       font_size=font_size,
                                       x=x,
                                       y=y,
                                       anchor_x=anchor_x,
                                       anchor_y=anchor_y,
                                       color=color)

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

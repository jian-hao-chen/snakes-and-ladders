# -*- coding: utf-8 -*-
"""Visualization of `Snakes and Ladders` environment.

Created on: 2020/11/09 15:49

Contents
"""
from gym.envs.classic_control import rendering

if __name__ == "__main__":
    viewer = rendering.Viewer(800, 600)

    @viewer.window.event
    def on_close():
        viewer.window_closed_by_user()
    
    while True:
        viewer.render()
        if not viewer.isopen:
            break

    viewer.close()
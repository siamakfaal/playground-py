from dataclasses import dataclass
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
from numpy import random


@dataclass
class GraphicHandles:
    figure: plt.Figure
    axes: List[plt.Axes]
    bars: List[plt.Rectangle]
    marble: plt.Line2D


class Pegboard:
    """
    Pegboard simulates marbles dropping on a triangular pegboard.
                  o
               o     o
               ...
         o   o   ...       o
       o   o   o         o   o
      [ ] [ ] [ ]  ...  [ ] [ ]
    """

    def __init__(self, bin_size: int = 10):
        self.bin_size = bin_size
        self.height = bin_size - 1
        self.bin = [0] * bin_size
        self.animate = False

    def simulate(self, iter: int = 100, animate: bool = False) -> list:

        if animate:
            handles = self._create_plot_env(iter)
            handles.marble.set_visible(True)
            plt.show()
        else:
            handles = None

        for _ in range(iter):
            self._drop(self.height / 2, self.height, handles)

        plt.ioff()
        print("Close figure to continue.")
        return self.bin

    def _drop(self, horizontal_pos: float, vertical_pos: int, handles: Union[None, GraphicHandles]):
        if handles:
            handles.marble.set_data([horizontal_pos], [vertical_pos])
            handles.figure.canvas.draw()
            handles.figure.canvas.flush_events()

        if vertical_pos > 0:
            direction = random.choice([-0.5, 0.5])
            self._drop(horizontal_pos + direction, vertical_pos - 1, handles)
        else:
            bin_index = int(horizontal_pos)
            self.bin[bin_index] += 1
            if handles:
                handles.bars[bin_index].set_height(self.bin[bin_index])
                handles.figure.canvas.draw()
                handles.figure.canvas.flush_events()

    def plot(self, results: list = None):
        if results is None:
            results = self.simulate()
        plt.bar(np.array(list(range(0, self.bin_size))), results)
        plt.show()

    def _create_plot_env(self, iter: int) -> GraphicHandles:
        pegboard_size = int(self.bin_size * (self.bin_size + 2) / 2)
        x = np.zeros(pegboard_size)
        y = np.zeros(pegboard_size)
        k = 0
        for level in range(0, self.height + 1):
            for i in range(self.bin_size - level):
                x[k] = level / 2 + i
                y[k] = level
                k += 1

        plt.ion()
        fig, ax = plt.subplots(2, 1)

        ax[0].scatter(x, y)
        (marble,) = ax[0].plot(0, 0, marker="o", color="red", markersize=10)

        ax[0].set_xlim((-1 / 2, self.bin_size - 1 / 2))
        ax[1].set_xlim((-1 / 2, self.bin_size - 1 / 2))
        ax[1].set_ylim((0, 2 * iter / 3))

        bars = ax[1].bar(np.array(list(range(0, self.bin_size))), np.zeros(self.bin_size))

        marble.set_visible(False)

        return GraphicHandles(fig, ax, list(bars), marble)

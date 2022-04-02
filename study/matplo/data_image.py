import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


class Draw:
    def __init__(self):
        self.font = FontProperties(fname='AaShiSong.ttf')

    def hist_nums(self, data: list, tick_label: list, title: str = None, x_name: str = None, y_name: str = None):
        fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
        ax.set_title(title, fontsize=16, fontproperties=self.font)
        ax.bar(range(len(tick_label)), data, color='b', width=0.25, tick_label=tick_label)
        for a, b in zip(range(len(tick_label)), data):
            ax.text(a, b + 0.1, b, ha='center', va='bottom', fontsize=14)
        # ax.grid(linestyle='--', alpha=0.5)
        plt.xlabel(x_name, fontsize=14)
        plt.ylabel(y_name, fontsize=14, rotation=0, loc='center', fontproperties=self.font)
        plt.show()

    def hist_oo(self, data, width, title: str = None, x_name: str = None, y_name: str = None):
        bins = self.bins(min(data), max(data), width)
        fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
        ax.set_title(title, fontsize=16, fontproperties=self.font)
        n, b, patches = ax.hist(data, bins=bins, density=True, color='b', alpha=0.5, rwidth=0.95)
        for a, b in zip(bins, n):
            if b != 0:
                ax.text(a + (bins[1]-bins[0])/2, b+0.1, int(b), ha='center', va='bottom', fontsize=14)

        ax.set_xticks(bins)
        ax.set_yticks(self.y_tick(n))
        ax.set_xlabel(x_name, fontsize=14, fontproperties=self.font)
        ax.set_ylabel(y_name, fontsize=14, rotation=0, fontproperties=self.font)
        plt.show()

    @classmethod
    def bins(cls, x_min, x_max, width):
        return np.arange(
            x_min,
            x_max + width,
            width)

    @classmethod
    def y_tick(cls, n):
        for i in [10000, 1000, 100, 10, 1]:
            if max(n) // i > 0:
                return range(0, int(max(n)+i), i)


if __name__ == '__main__':
    d = [100] * 156 + [200] * 345 + [500] * 1980
    t = 'GAGA'
    x = [1000, 2000, 3000, 4000]
    y = '哈哈'
    draw = Draw()
    draw.hist_oo(d, 50, y, y, y)

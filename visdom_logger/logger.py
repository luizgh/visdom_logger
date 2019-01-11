import visdom
import torch
from collections import defaultdict
import pickle
from enum import Enum


class ChartTypes(Enum):
    scalar = 1,
    scalars = 2,
    image = 3


class ChartData:
    def __init__(self):
        self.window = None
        self.type = None
        self.x_list = []
        self.y_list = []
        self.other_data = []


class VisdomLogger:
    def __init__(self, port):
        self.vis = visdom.Visdom(port=port)
        self.windows = defaultdict(lambda: ChartData())

    def scalar(self, name, x, y, title=""):
        data = self.windows[name]

        update = None if data.window is None else 'append'

        win = self.vis.line(torch.Tensor([y]), torch.Tensor([x]),
                            win=data.window, update=update, opts={'legend': [name], 'title': title})

        data.x_list.append(x)
        data.y_list.append(y)

        # Update the window
        data.window = win
        data.type = ChartTypes.scalar

    def scalars(self, list_of_names, x, list_of_ys, title=""):
        name = '$'.join(list_of_names)

        data = self.windows[name]

        update = None if data.window is None else 'append'
        list_of_xs = [x] * len(list_of_ys)
        win = self.vis.line(torch.Tensor([list_of_ys]), torch.Tensor([list_of_xs]),
                win=data.window, update=update, opts={'legend': list_of_names, 'title': title})

        data.x_list.append(x)
        data.y_list.append(list_of_ys)

        # Update the window
        data.window = win
        data.type = ChartTypes.scalars

    def images(self, name, images, mean_std=None, title=""):
        data = self.windows[name]

        if mean_std is not None:
            images = images * torch.Tensor(mean_std[0]) + torch.Tensor(mean_std[1])

        win = self.vis.images(images, win=data.window, opts={'legend': [name], 'title': title})

        # Update the window
        data.window = win
        data.other_data = images
        data.type = ChartTypes.image

    def reset_windows(self):
        self.windows.clear()

    def save(self, filename):
        to_save = {}
        for (name, data) in self.windows.items():
            to_save[name] = (torch.tensor(data.x_list, dtype=torch.float),
                             torch.tensor(data.y_list, dtype=torch.float),
                             torch.tensor(data.other_data, dtype=torch.float),
                             data.type)
        with open(filename, 'wb') as f:
            pickle.dump(to_save, f)

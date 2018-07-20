import visdom
import torch
from collections import defaultdict
import pickle
import argparse


class VisdomLogger:
    def __init__(self, port):
        self.vis = visdom.Visdom(port=port)
        self.windows = defaultdict(lambda: (None, None, None))

    def scalar(self, name, x, y):
        win, x_list, y_list = self.windows[name]

        update = None if win is None else 'append'
        x_list = x_list or []
        y_list = y_list or []

        win = self.vis.line(torch.Tensor([y]), torch.Tensor([x]),
                            win=win, update=update, opts={'legend': [name]})

        x_list.append(x)
        y_list.append(y)

        self.windows[name] = (win, x_list, y_list)

    def scalars(self, list_of_names, x, list_of_ys):
        name = '$'.join(list_of_names)

        win, x_list, y_list = self.windows[name]

        update = None if win is None else 'append'
        list_of_xs = [x] * len(list_of_ys)
        win = self.vis.line(torch.Tensor([list_of_ys]), torch.Tensor([list_of_xs]),
                            win=win, update=update, opts={'legend': list_of_names})

        self.windows[name] = (win, x_list, y_list)

    def images(self, name, images, mean_std=None):
        win, _, _ = self.windows[name]

        win = self.vis.images(images if mean_std is None else
                              images * torch.Tensor(mean_std[0]) + torch.Tensor(mean_std[1]),
                              win=win, opts={'legend': [name]})

        self.windows[name] = (win, None, None)

    def reset_windows(self):
        self.windows.clear()

    def save(self, filename):
        to_save = {name: (torch.tensor(x_list, dtype=torch.float), torch.tensor(y_list, dtype=torch.float)) for (name, (_, x_list, y_list)) in self.windows.items()}
        with open(filename, 'wb') as f:
            pickle.dump(to_save, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load visdom plots')
    parser.add_argument('filename', help='Filename with saved plots', required=True)
    parser.add_argument('-port', help='Visdom port', default=8097)

    args = parser.parse_args()
    vis = visdom.Visdom(port=port)

    with open(args.filename, 'rb') as f:
        loaded = pickle.load(f)

    for name, (x, y) in loaded.items():
        vis.line(y, x,  opts={'legend': [name]})

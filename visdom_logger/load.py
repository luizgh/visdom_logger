import visdom
import pickle
import argparse
from visdom_logger.logger import ChartTypes, ChartData


def load(filename, port):
    vis = visdom.Visdom(port=port)

    with open(filename, 'rb') as f:
        loaded = pickle.load(f)

    for name, (x, y, other_data, type) in loaded.items():
        if type == ChartTypes.scalar:
            vis.line(y, x, opts={'legend': [name]})
        elif type == ChartTypes.scalars:
            vis.line(y, x,  opts={'legend': name.split('$')})
        elif type == ChartTypes.image:
            vis.images(other_data, opts={'legend': [name]})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load visdom plots')
    parser.add_argument('filename', help='Filename with saved plots')
    parser.add_argument('-port', help='Visdom port', default=8097)

    args = parser.parse_args()

    load(args.filename, args.port)

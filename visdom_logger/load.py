import visdom
import pickle
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load visdom plots')
    parser.add_argument('filename', help='Filename with saved plots')
    parser.add_argument('-port', help='Visdom port', default=8097)

    args = parser.parse_args()
    vis = visdom.Visdom(port=args.port)

    with open(args.filename, 'rb') as f:
        loaded = pickle.load(f)

    for name, (x, y) in loaded.items():
        vis.line(y, x,  opts={'legend': [name]})

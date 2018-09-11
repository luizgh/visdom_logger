import os
import tempfile
import socket
import time
import torch
from multiprocessing import Process
import visdom.server as visdom_server
import visdom_logger
import visdom_logger.load


def _get_free_port():
    # From https://github.com/bethgelab/adversarial-vision-challenge/blob/master/bin/avc-test-model-against-attack
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_save_and_load():
    port = _get_free_port()

    visdom_server.download_scripts()
    p = Process(target=visdom_server.start_server, args=[port])
    p.start()

    time.sleep(1)  # Wait for visdom server

    # Create plots using the client
    client = visdom_logger.VisdomLogger(port=port)

    client.scalar('test', 0, 1)
    client.scalar('test', 1, 2)

    client.scalars(['a', 'b'], 0, [2, 4])
    client.scalars(['a', 'b'], 1, [4, 8])

    client.images('img', torch.zeros((5, 3, 32, 32)))

    temp_dir = tempfile.mkdtemp(prefix='visdomlogger')
    filename = os.path.join(temp_dir, 'save.pth')

    # Save
    client.save(filename)

    # Load
    visdom_logger.load.load(filename, port)

    p.terminate()

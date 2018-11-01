import os
from distutils.core import setup

requirements = [
    'visdom',
]

setup(
    name='visdom_logger',
    version="0.1",
    description='Visdom logger',
    author='Luiz Gustavo Hafemann',
    author_email='luiz.gh@mailbox.org',
    packages=['visdom_logger'],
    install_requires=requirements,
)

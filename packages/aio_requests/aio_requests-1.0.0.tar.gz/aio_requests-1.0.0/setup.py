#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name='aio_requests',
    version='1.0.0',
    description=(
        'An asynchronous request framework encapsulated with aiohttp '
    ),
    author='李渝',
    author_email='ly1334264106@163.com',
    maintainer='李渝',
    maintainer_email='ly1334264106@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/liyu133/aio_requests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'lxml',
        'cchardet',
        'aiohttp ',
    ]
)
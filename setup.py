#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    name='ORM-SQLite',
    version='0.0.1',
    description='A lightweight ORM for SQLite',
    author='Yi Zhang',
    author_email='yizhang.dev@gmail.com',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/yzhang-dev/ORM-SQLite',
    download_url='https://github.com/yzhang-dev/ORM-SQLite',
    packages=[
        'orm_sqlite'
    ],
    keywords=[
        'orm',
        'sqlite3',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    python_requires='>=3.7',
)

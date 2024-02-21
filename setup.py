#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

setup(
    name='verifier',
    version='0.0.0',
    license='Apache Software License 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[],
    project_urls={},
    keywords=[],
    python_requires='>=3.10.4',
    install_requires=[
        'hio>=0.6.9',
        'keri @ git+https://git@github.com/WebOfTrust/keripy.git@f1fa336ce4aaedfe80dff5c8efe7a609d8f56577',
        'falcon>=3.1.0',
    ],
    setup_requires=[],
    entry_points={
        'console_scripts': [
            'verifier = verifier.app:main',
        ]
    },
)

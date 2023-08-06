# encoding: utf-8
from __future__ import unicode_literals
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coordinates converter",
    version="0.0.2",
    author="Kristjan Tärk",
    author_email="kristjan.tark@gmail.com",
    description="L-Est97 to WGS84 coordinates converter with GUI interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyproj',
        'typing',
        'click'
    ],
    entry_points='''
        [console_scripts]
        coordinates-app=coordinates.client:start_app
    '''

)

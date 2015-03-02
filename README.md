# Summer Workshop on the Dynamic Brain
[Official Announcement](http://courses.washington.edu/braindyn/)

This repository provides a python wrapper library for accessing and manipulating voxel data from the Allen Mouse Connectivity Atlas (http://connectivity.brain-map.org/).
The library may be updated from time-to-time over the course, so if possible please check out a clone for easy updating.  Use python setup.py --version to check your version.

Check out the [wiki page](https://allendynamicbrain2014.wikispaces.com/Resources) for helpful resources

### Library Version:
Current version is defined [here](https://github.com/AllenBrainAtlas/friday-harbor/blob/master/setup.py)

### Library Examples:
Example scripts are located in ["examples" subdirectory](https://github.com/AllenBrainAtlas/friday-harbor/tree/master/examples)

## Installation

Install this package by:

    $ cd /path/to/repo.git
    $ python setup.py install

## Download the connectivity atlas (from a python terminal):

    $ from friday_harbor.data.regenerate_data import regenerate_data
    $ regenerate_data('/path/to/data/directory/')

## Dependencies (python packages):
	numpy/scipy
	h5py
	requests

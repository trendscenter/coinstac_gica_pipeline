#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 17:03:00 2018 (MDT)

@author: Rogers F. Silva
"""

import numpy as np


def listRecursive(d, key):
    for k, v in d.items():
        if isinstance(v, dict):
            for found in listRecursive(v, key):
                yield found
        if k == key:
            yield v


def read_data(file_list, file_type, clientId):
    """ Read data files.
    """
    if file_list:
        datasets = dict()  # Container for file contents
        for ix, filename in enumerate(file_list):

            if file_type == 'textfile':
                datasets[str(ix)] = np.loadtxt(filename)
            if file_type == 'npzfile':
                datasets[str(ix)] = np.load(filename)['dataset'].T
    else:
        raise ValueError("No files listed for site: {localID}".format(localID=clientId))

    return datasets

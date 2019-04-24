#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 17:03:00 2018 (MDT)

@author: Rogers F. Silva
"""

import numpy as np
import nibabel as nib
import pandas as pd
import os
import copy

COMPUTATION_OUTPUT = {
    "input": dict(),
    "output": dict(),
    "state": dict(),
    "cache": dict()
}


def default_computation_output(args, template=COMPUTATION_OUTPUT):
    computation_output = copy.deepcopy(template)
    for key in args.keys():
        computation_output[key] = args[key]
    return computation_output


def listRecursive(d, key):
    for k, v in d.items():
        if isinstance(v, dict):
            for found in listRecursive(v, key):
                yield found
        if k == key:
            yield v


def read_data_csv(filename, baseDir, clientId, data_colname="nii"):
    file_list = [
        os.path.join(baseDir, f)
        for f in list(pd.read_csv(filename)[data_colname])
    ]
    return read_data(file_list, "nii", clientId)


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
            if file_type == 'nii':
                datasets[str(ix)] = nib.load(filename).get_data()
    else:
        raise ValueError(
            "No files listed for site: {localID}".format(localID=clientId))

    return datasets

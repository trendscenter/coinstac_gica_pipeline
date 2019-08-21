#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 17:03:00 2018 (MDT)

@author: Rogers F. Silva
"""

import logging
import numpy as np
import nibabel as nib
import pandas as pd
import os
import copy
import utils as ut

COMPUTATION_OUTPUT = {
    "input": dict(),
    "output": dict(),
    "state": dict(),
    "cache": dict()
}


def resolve_args(args):
    default = default_computation_output(args)
    return default['state'], default['input'], default['cache']


def resolve_input(key, inputs=None, cache=None):
    if inputs and key in inputs.keys():
        return inputs[key]
    elif cache and key in cache.keys():
        return cache[key]
    else:
        raise (ValueError("Expected input with key %s in cache or inputs not detected." % key))


def log(msg, state):
    # create logger with 'spam_application'
    logger = logging.getLogger(state["clientId"])
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    if len(logger.handlers) == 0:
        filename = os.path.join(
            state["outputDirectory"], 'COINSTAC_%s.log' % state["clientId"])
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.INFO)
        # create console handler with a higher log level
        logger.addHandler(fh)
    logger.info(msg)


def default_computation_output(args, template=COMPUTATION_OUTPUT):
    computation_output = copy.deepcopy(template)
    for key in args.keys():
        computation_output[key] = args[key]
    return computation_output


def flatten_data(data, state):
    shp = data.shape
    if len(shp) >= 3:
        newshp = [np.prod(shp[:(len(shp)-1)]), shp[-1]]
        return np.reshape(data, newshp)
    return data


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


def read_file_list_csv(filename, baseDir, clientId, data_colname="nii"):
    file_list = [
        os.path.join(baseDir, f)
        for f in list(pd.read_csv(filename)[data_colname])
    ]
    return file_list


def read_data(base_directory, file_list, file_type, clientId):
    """ Read data files.
    """
    if file_list:
        datasets = dict()  # Container for file contents
        for ix, filename in enumerate(file_list):

            file = os.path.join(base_directory, filename);

            if file_type == 'textfile':
                datasets[str(ix)] = np.loadtxt(file)
            if file_type == 'npzfile':
                datasets[str(ix)] = np.load(file)['dataset'].T
            if file_type == 'nii':
                datasets[str(ix)] = np.array(nib.load(file).get_data())
    else:
        raise ValueError(
            "No files listed for site: {localID}".format(localID=clientId))

    return datasets

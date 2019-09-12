#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:08:00 2018 (MDT)

@author: Rogers F. Silva
"""

import scipy.io as sio
import logging
import pickle
import ujson as json
import os
import sys
import numpy as np
import utils as ut
import copy


def load_datasets(args, phase_prefix="local"):
    state = args['state']
    inputs = args['input']

    csv_file = os.path.join(state["baseDirectory"], inputs['datafile'][0])
    datasets = ut.read_data_csv(csv_file, state["baseDirectory"],
                                state["clientId"])

    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "datasets": datasets,
        "computation_phase": '%s_load_datasets' % phase_prefix
    }
    return computation_output


def noop(args, phase_prefix="local"):
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_noop' % phase_prefix
    }
    return computation_output


def cache_to_input(args, phase_prefix="local"):
    cache = args['cache']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_cache_to_input' % phase_prefix
    }
    for key in cache.keys():
        computation_output["input"][key] = cache[key]
    computation_output["cache"] = dict()
    return computation_output


def input_to_cache(args, phase_prefix="local"):
    inputs = args['input']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_input_to_cache' % phase_prefix
    }
    for key in inputs.keys():
        computation_output["cache"][key] = inputs[key]
    computation_output["input"] = dict()
    return computation_output

def input_to_output(args, phase_prefix="local"):
    inputs = args['input']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_input_to_cache' % phase_prefix
    }
    for key in inputs.keys():
        computation_output["output"][key] = inputs[key]
    return computation_output

def output_to_cache(args, phase_prefix="local"):
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_output_to_cache' % phase_prefix
    }
    for key in args["output"].keys():
        computation_output["cache"][key] = args["output"][key]
    return computation_output


def output_to_input(args, phase_prefix="local"):
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_output_to_input' % phase_prefix
    }
    for key in args["output"].keys():
        computation_output["input"][key] = args["output"][key]
    return computation_output


def dump_cache(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    out_file = os.path.join(state["outputDirectory"], "cache.json")
    json.dump(args["cache"], open(out_file,  "w", encoding="utf8"))
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache' % phase_prefix
    }
    return computation_output


def dump_cache_to_mat(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    out_file = os.path.join(state["outputDirectory"], "cache.mat")
    sio.savemat(out_file, args["cache"])
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache_to_mat' % phase_prefix
    }
    return computation_output


def dump_cache_to_npy(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    out_file = os.path.join(state["outputDirectory"], "cache.npy")
    np.save(out_file, args["cache"])
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache_to_npy' % phase_prefix
    }
    return computation_output


def load_cache(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    in_file = os.path.join(state["outputDirectory"], "cache.json")
    loaded = json.load(open(in_file,  "r", encoding="utf8"))
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache' % phase_prefix
    }
    for key in loaded.keys():
        computation_output["cache"][key] = loaded[key]

    return computation_output


def load_cache_from_npy(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    in_file = os.path.join(state["outputDirectory"], "cache.npy")
    loaded = np.load(in_file).item()
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache' % phase_prefix
    }
    for key in loaded.keys():
        computation_output["cache"][key] = loaded[key]

    return computation_output


def clear_cache(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_clear_cache' % phase_prefix
    }
    computation_output["cache"] = dict()
    return computation_output


def load_cache_from_file(args, filename=None, phase_prefix="local", keys=[], **kwargs):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    in_file = os.path.join(state["outputDirectory"], filename)
    prefix, ext = os.path.splitext(filename)
    loaded = dict()
    try:
        if 'npy' in ext:
            loaded = np.load(in_file).item()
        elif 'json' in ext:
            loaded = json.load(open(in_file, "r", encoding="utf8"))
        elif 'pkl' in ext:
            loaded = pickle.load(open(in_file, "r", encoding="utf8"))
        elif 'mat' in ext:
            loaded = sio.loadmat(in_file)
    except Exception:
        pass
    computation_output["output"] = {
        "computation_phase": '%s_load_cache' % phase_prefix
    }
    if len(keys) == 0:
        keys = loaded.keys()
    else:
        keys = [k for k in keys if k in loaded.keys()]
    for key in keys:
        computation_output["cache"][key] = loaded[key]
    return computation_output


def dump_cache_to_file(args, filename=None, phase_prefix="local", keys=[], **kwargs):
    state = args['state']
    cache = args['cache']
    if len(keys) == 0:
        keys = cache.keys()
    else:
        keys = [k for k in keys if k in cache.keys()]
    cache = {k: v for k, v in cache.items() if k in keys}
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    in_file = os.path.join(state["outputDirectory"], filename)
    prefix, ext = os.path.splitext(filename)
    loaded = dict()
    try:
        if 'npy' in ext:
            np.save(in_file, cache)
        elif 'json' in ext:
            json.dump(cache, open(in_file, "w"))
        elif 'pkl' in ext:
            pickle.load(cache, open(in_file, "w"))
        elif 'mat' in ext:
            sio.savemat(in_file, cache)
    except Exception as e:
        raise(Exception("Encountered an exception while saving data... %s" % e))
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache' % phase_prefix,
    }
    return computation_output

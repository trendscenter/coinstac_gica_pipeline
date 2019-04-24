#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:08:00 2018 (MDT)

@author: Rogers F. Silva
"""

import pickle
import json
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
    computation_output["success"] = True
    return computation_output


def noop(args, phase_prefix="local"):
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_noop' % phase_prefix
    }
    computation_output["success"] = True
    return computation_output


def cache_to_input(args, phase_prefix="local"):
    cache = args['cache']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_cache_to_input' % phase_prefix
    }
    computation_output["success"] = True
    for key in cache.keys():
        computation_output["input"][key] = cache[key]

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

    computation_output["success"] = True

    return computation_output


def output_to_cache(args, phase_prefix="local"):
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_output_to_cache' % phase_prefix
    }
    for key in args["output"].keys():
        computation_output["cache"][key] = args["output"][key]
    computation_output["success"] = True
    return computation_output


def dump_cache(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    out_file = os.path.join(state["outputDirectory"], "cache.pkl")
    pickle.dump(args["cache"], open(out_file, "wb"))
    computation_output["output"] = {
        "computation_phase": '%s_dump_cache' % phase_prefix
    }
    computation_output["success"] = True
    return computation_output


def clear_cache(args, phase_prefix="local"):
    state = args['state']
    # Compile results to be transmitted to remote and cached for reuse in next iteration
    computation_output = ut.default_computation_output(args)
    computation_output["output"] = {
        "computation_phase": '%s_clear_cache' % phase_prefix
    }
    computation_output["cache"] = dict()
    computation_output["success"] = True
    return computation_output

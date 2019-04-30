#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:07:00 2018 (MDT)

@author: Rogers F. Silva
"""

import ujson as json
import os
import sys
import numpy as np
import utils as ut
import copy
import phase_keys as pk
from constants import OUTPUT_TEMPLATE


REMOTE_SCICA_PHASES = \
    pk.SPATIALLY_CONSTRAINED_ICA_REMOTE + \
    pk.DFNC_PREPROC_REMOTE_EXEMPLARS + \
    pk.DFNC_PREPROC_REMOTE + \
    pk.DKMEANS_REMOTE + \
    pk.DKM_NOEX_REMOTE

if __name__ == '__main__':

    PIPELINE = REMOTE_SCICA_PHASES
    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(ut.listRecursive(parsed_args, 'computation_phase'))
    computation_output = copy.deepcopy(OUTPUT_TEMPLATE)
    ut.log("Starting remote phase %s" % phase_key, parsed_args["state"])
    ut.log("With input %s, and input keys %s" %
           (str(parsed_args.keys()), str(parsed_args['input'].keys())), parsed_args["state"])

    actual_cp = None

    for i, expected_phases in enumerate(PIPELINE):
        if expected_phases.get('recv') == phase_key or expected_phases.get('recv') in phase_key:
            operations = expected_phases.get('do')
            operation_args = expected_phases.get('args')
            operation_kwargs = expected_phases.get('kwargs')
            for operation, args, kwargs in zip(operations, operation_args, operation_kwargs):
                if 'input' in parsed_args.keys():
                    ut.log('Operation %s is getting input with keys %s' %
                           (operation.__name__, str(parsed_args['input'].keys())), parsed_args['state'])
                else:
                    ut.log('Operation %s is not getting any input!' % operation.__name__, parsed_args['state'])

                try:
                    ut.log("Trying operation %s, with args, and kwargs" %
                           (operation.__name__), parsed_args["state"])
                    computation_output = operation(parsed_args,
                                                   *args,
                                                   **kwargs)
                except NameError:
                    try:
                        ut.log("Trying operation %s, with kwargs only" %
                               (operation.__name__), parsed_args["state"])
                        computation_output = operation(parsed_args,
                                                       **kwargs)
                    except NameError:
                        try:
                            ut.log("Trying operation %s, with args only" %
                                   (operation.__name__), parsed_args["state"])
                            computation_output = operation(parsed_args,
                                                           *args)
                        except NameError:
                            ut.log("Trying operation %s, with no args or kwargs" %
                                   (operation.__name__), parsed_args["state"])
                            computation_output = operation(parsed_args)
                parsed_args = copy.deepcopy(computation_output)
                ut.log("Finished with operation %s" %
                       (operation.__name__), parsed_args["state"])
                ut.log("Operation output is %s, output keys %s" %
                       (str(parsed_args.keys()), str(parsed_args['output'].keys())), parsed_args["state"])
            if i+1 == len(PIPELINE):
                computation_output["success"] = True
            if expected_phases.get('send'):
                computation_output["output"]["computation_phase"] = expected_phases.get(
                    'send')
            ut.log("Finished with phase %s" %
                   expected_phases.get("send"), parsed_args["state"])
            break
    ut.log("Computation output looks like %s, and output keys %s" %
           (str(computation_output.keys()), str(computation_output["output"].keys())), parsed_args["state"])

    sys.stdout.write(json.dumps(computation_output))

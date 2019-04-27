#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:08:00 2018 (MDT)

@author: Rogers F. Silva
"""

import ujson as json
import os
import sys
import copy
import numpy as np
import utils as ut
import phase_keys as pk
from constants import OUTPUT_TEMPLATE


LOCAL_SCICA_PHASES = \
    pk.SPATIALLY_CONSTRAINED_ICA_LOCAL

if __name__ == '__main__':

    PIPELINE = LOCAL_SCICA_PHASES

    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(ut.listRecursive(parsed_args, 'computation_phase'))
    computation_output = copy.deepcopy(OUTPUT_TEMPLATE)
    ut.log("Starting phase %s" % phase_key, parsed_args["state"])
    for i, expected_phases in enumerate(PIPELINE):
        ut.log("Expecting phase %s, Got phase %s" %
               (expected_phases.get("recv"), phase_key), parsed_args["state"])
        if expected_phases.get('recv') == phase_key or expected_phases.get('recv') in phase_key:
            actual_cp = None
            operations = expected_phases.get('do')
            operation_args = expected_phases.get('args')
            operation_kwargs = expected_phases.get('kwargs')
            for operation, args, kwargs in zip(operations, operation_args, operation_kwargs):
                try:
                    ut.log("Trying operation %s, with args, and kwargs" %
                           (operation.__name__), parsed_args["state"])
                    computation_output = operation(parsed_args,
                                                   *args,
                                                   **kwargs)
                except NameError:
                    try:
                        ut.log("Trying operation %s, with args only" %
                               (operation.__name__), parsed_args["state"])
                        computation_output = operation(parsed_args,
                                                       *args)
                    except NameError:
                        try:
                            ut.log("Trying operation %s, with kwargs only" %
                                   (operation.__name__), parsed_args["state"])
                            computation_output = operation(parsed_args,
                                                           **kwargs)
                        except NameError:
                            ut.log("Trying operation %s, with no args or kwargs" %
                                   (operation.__name__), parsed_args["state"])
                            computation_output = operation(parsed_args)
                parsed_args = copy.deepcopy(computation_output)
                ut.log("Finished with operation %s" %
                       (operation.__name__), parsed_args["state"])
            computation_output["output"]["computation_phase"] = expected_phases.get(
                'send'
            )
            ut.log("Finished with phase %s" %
                   expected_phases.get("send"), parsed_args["state"])
            break
    ut.log("Full output is %s" %
           (str(computation_output)), parsed_args["state"])
    ut.log("Computation output looks like %s" %
           (str(computation_output["output"].keys())), parsed_args["state"])
    sys.stdout.write(json.dumps(computation_output))

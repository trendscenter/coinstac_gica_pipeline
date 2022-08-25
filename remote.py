#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:07:00 2018 (MDT)

@author: Bradley Baker

This file is a generic controller for remote computations based on the "phase_keys" computation design. This file controls the remote nodes.
The basic idea is that computations are designed to start on local nodes, and flow to the remote, then back again, and so on. 
At each switch between local and remote, a "phase_key" is sent from the local to remote and vice-versa to indicate the 
       location in the computation where local or remote node should continue. 
The phase_keys data structure is as follows:
       a python dictionary with three keys: "do", "recv" and "send".
       The "do" key holds a list, which has a list of function handles which are called in sequence. 
              The output from each function is directly fed as the input into the next function, and 
              the output from the final function is input to the next phase in the next decentralized iteration.
       The "recv" key is a string, which indicates the expected phase key to receive prior to computing. 
              **Local computations should expect to receive remote phase-keys and vice-versa**
       The "send" key is a string, which indicates the phase key to send to the next step in the computation. 
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
    pk.SPATIALLY_CONSTRAINED_ICA_REMOTE

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

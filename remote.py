#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:07:00 2018 (MDT)

@author: Rogers F. Silva
"""

import json
import os
import sys
import numpy as np
import utils as ut
import copy
import phase_keys as pk
from constants import OUTPUT_TEMPLATE

REMOTE_GICA_PHASES = \
    pk.ROW_MEANS_REMOTE + \
    pk.SPATIALLY_CONSTRAINED_ICA_REMOTE + \
    pk.DFNC_PREPROC_REMOTE + \
    pk.DKMEANS_REMOTE + \
    pk.DFNC_STATS_REMOTE

if __name__ == '__main__':
    parsed_args = json.loads(sys.stdin.read())
    phase_key = list(ut.listRecursive(parsed_args, 'computation_phase'))
    computation_output = copy.deepcopy(OUTPUT_TEMPLATE)
    for expected_phases in REMOTE_GICA_PHASES:
        if expected_phases.get('recv') == phase_key:
            operations = expected_phases.get('do')
            for operation in operations:
                computation_output = operation(**parsed_args)
                parsed_args = copy.deepcopy(computation_output)
            actual_cp = computation_output.get('output').get('computation_phase')
            expected_cp = expected_phases.get('send')
            assert (actual_cp == expected_cp), \
                "Received phase in Remote %s, Expected output phase %s, but instead got %s" % (
                    phase_key,
                    expected_cp,
                    actual_cp
            )
            break

""" Script to run all of the tests for Orca4
"""

__authors__ = "Kevin Moore"
__updated__ = "2019-01-13"

import os
import sys
import subprocess

# Get the PROGRAM and NODE from the user
PROGRAM = sys.argv[1]
HOSTNODE = sys.argv[2]

# Build a list with all of the input files
JOBDIRS = os.listdir('.')

# Loop through each input file and run the file
for jobdir in JOBDIRS:
    os.chdir(jobdir)
    subprocess.check_call(
        ['python',
         '/home/kmoore/elstruct-interface/submission/sblues.py',
         PROGRAM,
         HOSTNODE,
         '-b',
         'no'
         ]
    )
    os.chdir('../')

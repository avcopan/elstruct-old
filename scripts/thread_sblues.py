"""
Threads several jobs on Blues using the sblues script
"""

import os
import sys
import subprocess
from scripts.thread import tag_team_starmap


def sort_fxn(string):
    """ Sorts the directories by an underscore.
    """
    return int(string.split('_')[0])


def submit_fxn(jobpath, subcommand, hostnode):
    """ Function uses info to run the sblues script
    """

    # Change into the jobdir
    os.chdir(jobpath)

    # Run the submission command replacing HOST with the node
    subprocess.call([subcommand.replace('HOST', hostnode)])


# Get the lsit of directories containing each job
MAINPATH = os.getcwd()
JOBDIRS = os.listdir('.').sort(key=sort_fxn)

# Check for a jop params file and exit if it does not exist
if os.path.exists('./job_params.dat'):
    JOBDIRS.remove('job_params.dat')
else:
    print('Need a job_params.dat file specifying job params')
    sys.exit()

# Append full paths to all of the job directories
JOBPATHS = [MAINPATH+jobdir for jobdir in JOBDIRS]

# Open the thread file and read in the job parameters
with open('job_params.dat', 'r') as paramfile:
    for line in paramfile:
        if 'hostnodes =' in line:
            hostnodes = line.strip().split()[2:]
        if 'command =' in line:
            command = line.strip().split()[2:]
SUBCOMMANDS = [command for i in range(len(JOBPATHS))]

# Zip the paths and commands to pass into submission function
SUBMIT_ARGS = tuple(zip(JOBPATHS, SUBCOMMANDS))

# Call the submssion function
tag_team_starmap(submit_fxn, SUBMIT_ARGS, hostnodes)

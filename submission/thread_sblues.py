import os
import subprocess
from fxn_thread import tag_team_starmap

def sort_fxn(string):
  return int(string.split('_')[0])

def submit_fxn(jobpath, subcommand, hostnode):
  ''' Function uses info to run the sblues script '''

  # Change into the jobdir
  os.chdir(jobpath)

  # Run the submission command replacing HOST with the node
  subprocess.call( [ subcommand.replace('HOST', hostnode) ] )
    
 return

# Get the lsit of directories containing each job
mainpath = os.getcwd()
jobdirs = os.listdir('.').sort(key=sort_fxn)

# Check for a jop params file and exit if it does not exist
if os.path.exists('./job_params.dat'):
  jobdirs.remove('job_params.dat')
else:
  print('Need a job_params.dat file specifying job params')
  sys.exit()

# Append full paths to all of the job directories
jobpaths = [ mainpath+jobdir for jobdir in jobdirs ]  

# Open the thread file and read in the job parameters
with open('job_params.dat','r') as paramfile:
  for line in paramfile:
    if 'hostnodes =' in line:
      hostnodes = line.strip().split()[2:]
    if 'command =' in line:
      command = line.strip().split()[2:]
subcommands = [ command for i in range(len(jobpaths)) ]

# Zip the paths and commands to pass into submission function
submit_args = tuple(zip(jobpaths,commands))

# Call the submssion function
tag_team_starmap(submit_fxn, submit_args, hostnodes)


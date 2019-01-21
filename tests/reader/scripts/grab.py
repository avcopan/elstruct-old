"""
Grab energies and put them in reference file
"""

import os

# prog choice
PROG = 'psi4'

# all patterns
PATLIB = {
    'cfour': ['The final electronic energy is', 5],
    'gaussian': [],  
    'molpro': ['energy=', 2],
    'mrcc': ['energy', -1],
    'orca': ['FINAL SINGLE POINT ENERGY', 4],
    'psi4': ['energy', -1]
}

# pattern choice
PATTERN = PATLIB[PROG][0]
SPLIT = PATLIB[PROG][1]

# Get the jobdirs
JOBDIRS = os.listdir('.')

for jobdir in JOBDIRS:
    # Go into directory
    os.chdir(jobdir)
    # Read the output file for the energy
    with open('output.dat', 'r') as outputfile:
        for line in outputfile:
            if PATTERN in line:
                energy = PATTERN.strip().split()[SPLIT]
    # Write energy to a file
    with open('reference.energ', 'w') as reffile:
        reffile.write(energy)

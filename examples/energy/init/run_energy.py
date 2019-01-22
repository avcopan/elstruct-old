"""
  Run all the modules succinctly
"""

import os
from elstruct import iohelp
from elstruct import writer
from elstruct import runner
from elstruct import reader


# INITIAL SET-UP FOR VARIABLES #

# Set electronic structure code to run
PROGRAM = 'molpro2015'

# Set level of theory for writer and reader
METHOD = 'rhf-ccsd'
BASIS = '6-31G*'

# Set molecular specifications for writer
CHARGE = 0
MULT = 1

# Obtain geometry from xyz file for writer
WORK_PATH = os.getcwd()
INIT_GEOM_PATH = os.path.join(WORK_PATH, 'water.xyz')
INIT_CART_GEOM = iohelp.read_cartesian_geometry(INIT_GEOM_PATH)
COORD_SYS = 'xyz'

# Set computer specs for runtime used by writer and runner
INPUT_FILE_NAME = 'input.dat'
MEMORY = 20
HOSTNODES = 'b444'
NCORES_PER_NODE = 4
BACKGROUND = False


# WRITER MODULE #

# Obtain input string using the writer function
INPUT_STR = writer.energy(PROGRAM, INPUT_FILE_NAME, METHOD, BASIS,
                          INIT_CART_GEOM, COORD_SYS, CHARGE, MULT,
                          memory=MEMORY)
# Write string to file
with open(INPUT_FILE_NAME, 'w') as input_file:
    input_file.write(INPUT_STR)


# RUNNER MODULE #

# Submit job to Blues node
runner.blues(
    PROGRAM, HOSTNODES,
    ncores_per_node=NCORES_PER_NODE,
    background=BACKGROUND)


# READER MODULE #

# Obtain output string that would be passed to reader function
with open('output.dat') as out_file:
    OUTPUT_STR = out_file.read()

# Retrieve the energy, geom, freqs, and zpve of optimized geometry
ENERGY = reader.energy(PROGRAM, METHOD, OUTPUT_STR)
# GEOM = reader.optimized_cartesian_geometry.(PROGRAM, OUTPUT_STR)
# FREQS = reader.harmonic_frequencies(PROGRAM, OUTPUT_STR)
# ZPVE = reader.harmonic_zero_point_vibrational_energy(PROGRAM, OUTPUT_STR)

# Write each of these values to a file for storage
iohelp.write_energy('water', ENERGY)
# iohelp.write_energy('geom.xyz', ENERGY)
# iohelp.write_energy('freqs.dat', ENERGY)
# iohelp.write_energy('zpve.dat', ENERGY)

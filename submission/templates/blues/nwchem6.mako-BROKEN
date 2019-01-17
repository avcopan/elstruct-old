#!/bin/bash

# Set current working directory
CWD=${workdir}

# Set host
HOST=${hostnodes}

# Set variables for NWChem
export NWCHEMEXE=/soft/nwchem/bebop/bdw-casper/bin/nwchem 

# Load intel and MPI libraries
soft add +mvapich2-2.2b-intel-15.0
soft add +intel-15.0
soft add +libpciaccess-0.13.4
soft add +libxml2-2.9.4

# Set MPI
export I_MPI_FABRICS=shm:tmi
export I_MPI_OFI_PROVIDER=psm2

# Include Casper library in LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/soft/nwchem/bebop/bdw-casper/lib/libcasper.so:$LD_LIBRARY_PATH

# Set the scratch directory
export TMPDIR=${scratch}

# Set runtime options for MPI
MPI_OPTIONS="-n ${ncores_total} -ppn ${ncores_per_node} -hosts $HOST"

# Run NWCHEM with MPIs
% if background == 'yes':
mpirun $MPI_OPTION $NWCHEMEXE $CWD/${input} > $CWD/${output} &
% else:
mpirun $MPI_OPTION $NWCHEMEXE $CWD/${input} > $CWD/${output} 
% endif


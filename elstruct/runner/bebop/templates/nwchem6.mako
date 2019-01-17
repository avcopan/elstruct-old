#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N ${nnodes}
#SBATCH --ntasks-per-node=${ncores_per_node}
#SBATCH -t ${walltime}
#SBATCH -J ${jobname}
#SBATCH -A ${account}
#SBATCH -o job_%j.log
#SBATCH -e job_%j.err

# Set variables for NWChem
export NWCHEMEXE=/soft/nwchem/bebop/bdw-casper/bin/nwchem 

# Set MPI
export I_MPI_FABRICS=shm:tmi
export I_MPI_OFI_PROVIDER=psm2

# Include Casper library in LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/soft/nwchem/bebop/bdw-casper/lib/libcasper.so

# Set the scratch directory
export TMPDIR=${scratch}

# Run NWCHEM with MPI
% if background == 'yes':
srun $NWCHEMEXE $SLURM_SUBMIT_DIR/${input} > $SLURM_SUBMIT_DIR/${output} &
% else:
srun $NWCHEMEXE $SLURM_SUBMIT_DIR/${input} > $SLURM_SUBMIT_DIR/${output} 
% endif


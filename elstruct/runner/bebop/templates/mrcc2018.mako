#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N 1
#SBATCH --ntasks=${ncores_per_node}
#SBATCH -t ${walltime}
#SBATCH -J ${jobname}
#SBATCH -A ${account}
#SBATCH -o job_%j.log
#SBATCH -e job_%j.err

# Add executables for executable
export PATH=$PATH:/lcrc/project/PACC/brossdh/mrcc/
MRCCEXE=$(which dmrcc)

# Load Intel parallel studio 
module load intel-parallel-studio/cluster.2018.1-egcacag

# Set num threads for OpenMP
export OMP_NUM_THREADS=$SLURM_NTASKS

# Create the scratch irectory
export TMPDIR=${scratch}
mkdir -p $TMPDIR

# Copy file from scratch
cp $SLURM_SUBMIT_DIR/${input} $TMPDIR/MINP

# Change into scratch directory
cd $TMPDIR

# Run MRCC with srun for MPI para
% if background == 'yes':
$MRCCEXE >& $SLURM_SUBMIT_DIR/${output} &
% else:
$MRCCEXE >& $SLURM_SUBMIT_DIR/${output} 
% endif

# Go back to working directory
cd $SLURM_SUBMIT_DIR



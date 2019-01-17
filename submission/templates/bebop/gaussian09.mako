#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N 1
#SBATCH --ntasks-per-node=${ncores_per_node}
#SBATCH -t ${walltime}
#SBATCH -J ${jobname}
#SBATCH -A ${account}
#SBATCH -o job_%j.log
#SBATCH -e job_%j.err

# Load Gaussian
module load gaussian/09-e.01

# Set sratch directory
export GAUSS_SCRDIR=${scratch}
mkdir -p $GAUSS_SCRDIR 

# Run Gaussian
% if background == 'yes':
g09 -scrdir=$GAUSS_SCRDIR < $SLURM_SUBMIT_DIR/${input} > $SLURM_SUBMIT_DIR/${output} &
% else:
g09 -scrdir=$GAUSS_SCRDIR < $SLURM_SUBMIT_DIR/${input} > $SLURM_SUBMIT_DIR/${output} 
% endif


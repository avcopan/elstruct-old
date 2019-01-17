#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N 1
#SBATCH --ntasks-per-node=${ncores_per_node}
#SBATCH -t ${walltime}
#SBATCH -J ${jobname}
#SBATCH -A ${account}
#SBATCH -o job_%j.log
#SBATCH -e job_%j.err

# Run Psi4
% if background == 'yes':
psi4 -n $SLURM_NTASKS_PER_NODE -i $SLURM_SUBMIT_DIR/${input} -o $SLURM_SUBMIT_DIR/${output} &
% else:
psi4 -n $SLURM_NTASKS_PER_NODE -i $SLURM_SUBMIT_DIR/${input} -o $SLURM_SUBMIT_DIR/${output} 
% endif


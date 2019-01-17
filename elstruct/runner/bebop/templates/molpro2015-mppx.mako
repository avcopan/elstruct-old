#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N ${nnodes}
#SBATCH --ntasks-per-node=${ncores_per_node}
#SBATCH -t ${walltime}
#SBATCH -J ${jobname}
#SBATCH -A ${account}
#SBATCH -o job_%j.log
#SBATCH -e job_%j.err

# Set enviornmental variables for MPI
export I_MPI_FABRICS=shm:tmi

# Load Molpro
module load molpro/2015.1_170920

# Set Molpro library directory
MOLPRO_LIB=/soft/molpro/2015.1_170920/bebop/molprop_2015_1_linux_x86_64_i8/lib/

# Set the scratch directory
export TMPDIR=${scratch}

# Set runtime options for Molpro
MOLPRO_OPTIONS="--mppx --nouse-logfile --no-xml-output -L $MOLPRO_LIB -d $TMPDIR -I $TMPDIR -W $TMPDIR -o ${output}"

# Run Molpro with mpirun for MPI parallelization
% if background == 'yes':
srun molpro.exe $MOLPRO_OPTIONS $SLURM_SUBMIT_DIR/${input} &
% else:
srun molpro.exe $MOLPRO_OPTIONS $SLURM_SUBMIT_DIR/${input}
% endif


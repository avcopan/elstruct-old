#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N ${nnodes}
% if njobs == 1:
#SBATCH --ntasks-per-node=${ncores_per_node}
% else:
#SBATCH --cpus-per-task=${ncores_per_node}
% endif
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
% if njobs == 1:
MOLPRO_OPTIONS="--nouse-logfile --no-xml-output -L $MOLPRO_LIB -d $TMPDIR -I $TMPDIR -W $TMPDIR -o $SLURM_SUBMIT_DIR/${output}"
% else:
% for i in range(njobs):
MOLPRO_OPTIONS${i+1}="--nouse-logfile --no-xml-output -L $MOLPRO_LIB -d $TMPDIR -I $TMPDIR -W $TMPDIR -o $SLURM_SUBMIT_DIR/calc${i+1}/${output}"
% endfor
% endif

# Run Molpro with mpirun for MPI parallelization
% if njobs == 1:
  % if background == 'yes':
srun molpro.exe $MOLPRO_OPTIONS $SLURM_SUBMIT_DIR/${input} &
  % else:
srun molpro.exe $MOLPRO_OPTIONS $SLURM_SUBMIT_DIR/${input}
  % endif
% else:
  % for i in range(njobs):
    % if background == 'yes':
srun -c 1 -n ${ncores_per_node} --exclusive molpro.exe $MOLPRO_OPTIONS${i+1} $SLURM_SUBMIT_DIR/calc${i+1}/${input} &
    % else:
srun -c 1 -n ${ncores_per_node} --exclusive molpro.exe $MOLPRO_OPTIONS${i+1} $SLURM_SUBMIT_DIR/calc${i+1}/${input} 
    % endif
  % endfor
wait
% endif


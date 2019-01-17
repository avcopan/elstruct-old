#!/bin/sh

# Set current working directory
CWD=${workdir}

# Set host
HOST=${hostnodes}

# Load Molpro 
soft add +molpro-2015.1-mvapich2
MOLPROEXE=$(which molpro.exe)

# Load intel and MPI libraries
soft add +mvapich2-2.2b-intel-15.0
soft add +intel-15.0
soft add +libpciaccess-0.13.4
soft add +libxml2-2.9.4

# Load GCC library 
soft add +gcc-4.7.2

# Set Molpro library directory
MOLPRO_LIB=/soft/molpro/2015.1_mvapich2/lib/

# Set the Molpro scratch directory
TMPDIR=${scratch}

# Set runtime options for MPI
MPI_OPTIONS="-n ${ncores_total} -ppn ${ncores_per_node} -hosts $HOST"

# Set runtime options for Molpro
% if njobs == 1:
MOLPRO_OPTIONS="--nouse-logfile --no-xml-output -L $MOLPRO_LIB -d $TMPDIR -I $TMPDIR -W $TMPDIR -o $CWD/${output}"
% else:
% for i in range(njobs):
MOLPRO_OPTIONS${i+1}="--nouse-logfile --no-xml-output -L $MOLPRO_LIB -d $TMPDIR -I $TMPDIR -W $TMPDIR -o $CWD/calc${i+1}/${output}"
% endfor
% endif

# Run the molpro executable
% if njobs == 1:
 % if background == 'yes':
mpirun $MPI_OPTIONS $MOLPROEXE $MOLPRO_OPTIONS $CWD/${input} &
 % else:
mpirun $MPI_OPTIONS $MOLPROEXE $MOLPRO_OPTIONS $CWD/${input} 
 % endif
% else:
 % for i in range(njobs):
  % if background == 'yes':
mpirun $MPI_OPTIONS $MOLPROEXE $MOLPRO_OPTIONS${i+1} $CWD/calc${i+1}/${input} &
  % else:
mpirun $MPI_OPTIONS $MOLPROEXE $MOLPRO_OPTIONS${i+1} $CWD/calc${i+1}/${input} 
  % endif
 % endfor
% endif


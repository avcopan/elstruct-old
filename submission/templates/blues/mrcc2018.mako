#!/bin/bash

# Set path
CWD=${workdir}

# Set host node to the one specified by the user
HOST=${hostnodes}

# Add executables for executable
export PATH=/lcrc/project/PACC/brossdh/mrcc_blues:$PATH
MRCCEXE=$(which dmrcc)

# Set num threads for OpenMP
export OMP_NUM_THREADS=${ncores_per_node}

# Create the scratch irectory
export TMPDIR=${scratch}
timestamp=$(date +%s%9N)
export SCRDIR=$TMPDIR/MRCCSCR_$timestamp

# SSH into node
ssh -n $HOST " soft add +intel-parallel-studio-17.0.4                            ;
               export PATH=$PATH                                                 ;
               export OMP_NUM_THREADS=$OMP_NUM_THREADS                           ;
               mkdir -p $TMPDIR                                                  ;
               mkdir -p $SCRDIR                                                  ;
               cp $CWD/${input} $SCRDIR/MINP                                     ;
               cd $TMPDIR                                                        ;
               cd $SCRDIR                                                        ;
               $MRCCEXE >& $CWD/${output}                                        ;
               cd $TMPDIR                                                        ;
               rm -r MRCCSCR_$timestamp                                          ;
               cd $CWD                                                             " \
% if background == 'yes':
               &
% endif 


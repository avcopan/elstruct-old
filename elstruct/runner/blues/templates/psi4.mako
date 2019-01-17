#!/bin/bash

# Set current working directory
CWD=${workdir}

# Set host node to the one specified by the user
HOST=${hostnodes}

# Set the scratch directory
TMPDIR=${scratch}

# Run Psi4
ssh -n $HOST " conda activate esenv                                          ;
               mkdir -p $TMPDIR                                              ;
               psi4 -n ${ncores_per_node} -i $CWD/${input} -o $CWD/${output} " \
% if background == 'yes':
               &
% endif

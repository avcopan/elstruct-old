#!/bin/bash

# Set path
CWD=${workdir}

# Set host node to the one specified by the user
HOST=${hostnodes}

# Set the scratch directory
export GAUSS_SCRDIR=${scratch}                                

# SSH into the Blues node and run Gaussian
ssh -n $HOST " soft add +g09-e.01                                         ; 
               mkdir -p $GAUSS_SCRDIR                                     ; 
               g09 -scrdir=$GAUSS_SCRDIR < $CWD/${input} > $CWD/${output}  " \
% if background == 'yes':
               &
% endif


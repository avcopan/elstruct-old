#!/bin/bash

# Set path
CWD=/blues/gpfs/home/kmoore/elstruct/tests/reader/data/cartesian_gradient/gaussian09/cartesian

# Set host node to the one specified by the user
HOST=b432

# Set the scratch directory
export GAUSS_SCRDIR=/scratch/$USER                                

# SSH into the Blues node and run Gaussian
ssh -n $HOST " soft add +g09-e.01                                                          ; 
               mkdir -p $GAUSS_SCRDIR                                                      ; 
               g09 -scrdir=$GAUSS_SCRDIR < $CWD/input.dat > $CWD/output.dat                   "                &


#!/bin/bash

# Set path to the working directory
CWD=${workdir}

# Set host node to the one specified by the user
HOST=${hostnodes}

# Set paths to Orca and MPI
export PATH=/soft/orca/orca_4_0_1_2_linux_x86-64_openmpi202:/soft/spack-0.10.0/opt/spack/linux-centos6-x86_64/intel-17.0.2/openmpi-2.0.2-pyxkvzeiklfv4v67y46xheicu5j2no4v/bin:$PATH
export LD_LIBRARY_PATH=/soft/spack-0.10.0/opt/spack/linux-centos6-x86_64/intel-17.0.2/openmpi-2.0.2-pyxkvzeiklfv4v67y46xheicu5j2no4v/lib:$LD_LIBRARY_PATH
export ORCAEXE=$(which orca)

# Set variable for the scratch directory
export TMPDIR=${scratch}
timestamp=$(date +%s%9N)
export SCRDIR=$TMPDIR/ORCASCR_$timestamp

# SSH into Blues node, run Orca, and copy any data from job
ssh -n $HOST " export PATH=$PATH                                                             ;
               export LD_LIBRARY_PATH=$LD_LIBRARY_PATH                                       ;
               mkdir -p $TMPDIR                                                              ;
               mkdir -p $SCRDIR                                                              ;
               cp $CWD/input.dat $SCRDIR/input.dat                                           ;
               if [ -e $CWD/input.xyz  ]; then cp $CWD/input.xyz  $SCRDIR/guess.xyz  ; fi    ;
               if [ -e $CWD/input.gbw  ]; then cp $CWD/input.gbw  $SCRDIR/guess.gbw  ; fi    ;
               if [ -e $CWD/input.hess ]; then cp $CWD/input.hess $SCRDIR/guess.hess ; fi    ;
               if [ -e $CWD/input.pot  ]; then cp $CWD/input.pot  $SCRDIR/guess.pot  ; fi    ;
               $ORCAEXE $SCRDIR/input.dat > $CWD/output.dat 2>> $CWD/err                     ;
               mkdir -p $CWD/Job_Data                                                        ;
               cp $SCRDIR/*.xyz  $CWD/Job_Data 2>> $CWD/err                                  ;
               cp $SCRDIR/*.gbw  $CWD/Job_Data 2>> $CWD/err                                  ;
               cp $SCRDIR/*.hess $CWD/Job_Data 2>> $CWD/err                                  ;
               cp $SCRDIR/*.pot  $CWD/Job_Data 2>> $CWD/err                                  ;
               cd $TMPDIR                                                                    ;
               rm -r ORCASCR_$timestamp                                                      ;
               cd $CWD                                                                         " \
% if background == 'yes':
               &
% endif


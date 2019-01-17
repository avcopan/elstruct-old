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

# SSH into Blues node, run Orca, and copy any data from job
ssh -n $HOST " mkdir -p $TMPDIR                                                              ;
               export PATH=$PATH                                                             ;
               export LD_LIBRARY_PATH=$LD_LIBRARY_PATH                                       ;
               cp $CWD/input.dat $TMPDIR/input.dat                                           ;
               if [ -e $CWD/input.xyz  ]; then cp $CWD/input.xyz  $TMPDIR/guess.xyz  ; fi    ;
               if [ -e $CWD/input.gbw  ]; then cp $CWD/input.gbw  $TMPDIR/guess.gbw  ; fi    ;
               if [ -e $CWD/input.hess ]; then cp $CWD/input.hess $TMPDIR/guess.hess ; fi    ;
               if [ -e $CWD/input.pot  ]; then cp $CWD/input.pot  $TMPDIR/guess.pot  ; fi    ;
               $ORCAEXE $TMPDIR/input.dat > $CWD/output.dat 2>> $CWD/log                     ;
               mkdir -p $CWD/Job_Data                                                        ;
               cp $TMPDIR/*.xyz  $CWD/Job_Data 2>> $CWD/log                                  ;
               cp $TMPDIR/*.gbw  $CWD/Job_Data 2>> $CWD/log                                  ;
               cp $TMPDIR/*.hess $CWD/Job_Data 2>> $CWD/log                                  ;
               cp $TMPDIR/*.pot  $CWD/Job_Data 2>> $CWD/log                                   " \
% if background == 'yes':
               &
% endif


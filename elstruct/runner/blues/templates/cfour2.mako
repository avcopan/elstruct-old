#!/bin/bash

# Set path
CWD=${workdir}

# Set host node to the one specified by the user
HOST=${hostnodes}

# Add CFOUR executables to PATH and set full path to Orca executable to have access to all Orca binaries at runtime
export PATH=/lcrc/project/PACC/brossdh/cfour_blues/bin:$PATH
CFOUREXE=$(which xcfour)
CFOURXJA=$(which xja2fja)
CFOURBASIS=/lcrc/project/PACC/brossdh/cfour_blues/basis/

# Set variables for parallelization 
nproc=`grep -c ^processor /proc/cpuinfo`
export CFOUR_NUM_CORES=${ncores_per_node}
export OMP_NUM_THREADS=`echo 'scale=0;'$nproc'/'$CFOUR_NUM_CORES | bc`

# Set the scratch and current working directory
export TMPDIR=${scratch}

# SSH into Blues node, run CFOUR, and copy any data from job
ssh -n $HOST " soft add +intel-parallel-studio-17.0.4     ;
               export PATH=$PATH                          ;
               export CFOUR_NUM_CORES=$CFOUR_NUM_CORES    ;
               export OMP_NUM_THREADS=$OMP_NUM_THREADS    ;
               mkdir -p $TMPDIR                           ;
               cp $CWD/${input} $TMPDIR/ZMAT              ;
               cp $CFOURBASIS/GENBAS $TMPDIR/GENBAS       ;
               cp $CFOURBASIS/ECPDATA $TMPDIR/ECPDATA     ;
               cd $TMPDIR                                 ;
               $CFOUREXE >& $CWD/${output}                ;
               $CFOURXJA > $CWD/xja_out.dat               ;
               mkdir -p $CWD/Job_Data                     ;
               cp $TMPDIR/den.dat  $CWD/Job_Data/den.dat  ;
               cp $TMPDIR/FCMINT   $CWD/Job_Data/FCMINT   ;
               cp $TMPDIR/FCMFINAL $CWD/Job_Data/FCMFINAL ;
               cp $TMPDIR/JOBARC   $CWD/Job_Data/JOBARC   ;
               cp $TMPDIR/JAINDX   $CWD/Job_Data/JAINDX   ;
               cp $TMPDIR/MOLDEN   $CWD/Job_Data/MOLDEN   ;
               cp $TMPDIR/ZMATnew  $CWD/ZMATnew           ;
               if [ -e "$TMPDIR/zmat001" ]; then mkdir $CWD/Disps ; cp $TMPDIR/zmat* $CWD/Disps ; fi ;
               if [ -e "$TMPDIR/FJOBARC"  ]; then cp $TMPDIR/FJOBARC $CWD/Job_Data/FJOBARC      ; fi ;
               cd $CWD                                                                                 " \
% if background == 'yes':
               &
% endif


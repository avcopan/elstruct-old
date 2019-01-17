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
timestamp=$(date +%s%9N)
export SCRDIR=$TMPDIR/CFOURSCR_$timestamp

# SSH into Blues node, run CFOUR, and copy any data from job
ssh -n $HOST " soft add +intel-parallel-studio-17.0.4     ;
               export PATH=$PATH                          ;
               export CFOUR_NUM_CORES=$CFOUR_NUM_CORES    ;
               export OMP_NUM_THREADS=$OMP_NUM_THREADS    ;
               mkdir -p $TMPDIR                           ;
               mkdir -p $SCRDIR                           ;
               cp $CWD/${input} $SCRDIR/ZMAT              ;
               cp $CFOURBASIS/GENBAS $SCRDIR/GENBAS       ;
               cp $CFOURBASIS/ECPDATA $SCRDIR/ECPDATA     ;
               cd $SCRDIR                                 ;
               $CFOUREXE >& $CWD/${output}                ;
               $CFOURXJA >& $CWD/xja_out.dat              ;
               mkdir -p $CWD/Job_Data                     ;
               cp $SCRDIR/den.dat  $CWD/Job_Data/den.dat  ;
               cp $SCRDIR/FCMINT   $CWD/Job_Data/FCMINT   ;
               cp $SCRDIR/FCMFINAL $CWD/Job_Data/FCMFINAL ;
               cp $SCRDIR/JOBARC   $CWD/Job_Data/JOBARC   ;
               cp $SCRDIR/JAINDX   $CWD/Job_Data/JAINDX   ;
               cp $SCRDIR/MOLDEN   $CWD/Job_Data/MOLDEN   ;
               cp $SCRDIR/ZMATnew  $CWD/ZMATnew           ;
               if [ -e "$SCRDIR/zmat001" ]; then mkdir $CWD/Disps ; cp $SCRDIR/zmat* $CWD/Disps ; fi ;
               if [ -e "$SCRDIR/FJOBARC"  ]; then cp $SCRDIR/FJOBARC $CWD/Job_Data/FJOBARC      ; fi ;
               cd $TMPDIR                                                                            ; 
               rm -r CFOURSCR_$timestamp                                                             ;
               cd $CWD                                                                                 " \
% if background == 'yes':
               &
% endif


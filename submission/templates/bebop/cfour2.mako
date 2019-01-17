#!/bin/bash
#SBATCH -p ${partition}
#SBATCH -N 1
#SBATCH --ntasks=${ncores_per_node}
#SBATCH -t ${walltime}
#SBATCH -J ${jobname}
#SBATCH -A ${account}
#SBATCH -o job_%j.log
#SBATCH -e job_%j.err

# Load Intel parallel studio 
module load intel-parallel-studio/cluster.2018.1-egcacag

# Add CFOUR executables to PATH and set full path to Orca executable to have access to all Orca binaries at runtime
export PATH=/lcrc/project/PACC/brossdh/openmpi/bin:/lcrc/project/PACC/brossdh/cfour_mpi_openmpi/bin:$PATH
export LD_LIBRARY_PATH=/lcrc/project/PACC/brossdh/openmpi/lib:$LD_LIBRARY_PATH
CFOUREXE=$(which xcfour)
CFOURXJA=$(which xja2fja)
CFOURBASIS=/lcrc/project/PACC/brossdh/cfour_mpi_openmpi/basis/

# Set variables for parallelization 
nproc=`grep -c ^processor /proc/cpuinfo`
export CFOUR_NUM_CORES=$SLURM_NTASKS
export OMP_NUM_THREADS=`echo 'scale=0;'$nproc'/'$CFOUR_NUM_CORES | bc`

# Set the scratch and current working directory
export TMPDIR=${scratch}
mkdir -p $TMPDIR

# Copy file from scratch
cp $SLURM_SUBMIT_DIR/${input} $TMPDIR/ZMAT

# Copy files with the basis set and ECP, checking first if one is in working dir 
if [ -e $SLURM_SUBMIT_DIR/GENBAS   ]; then 
  cp $SLURM_SUBMIT_DIR/GENBAS  $TMPDIR/GENBAS 
else
  cp $CFOURBASIS/GENBAS  $TMPDIR/GENBAS 
fi 

if [ -e $SLURM_SUBMIT_DIR/ECPDATA  ]; then 
  cp $SLURM_SUBMIT_DIR/ECPDATA  $TMPDIR/ECPDATA 
else
  cp $CFOURBASIS/ECPDATA  $TMPDIR/ECPDATA
fi 

# Copy files with guess orbitals, Hessian 
if [ -e $SLURM_SUBMIT_DIR/initden.dat  ]; then cp $SLURM_SUBMIT_DIR/initden.dat  $TMPDIR/initden.dat  ; fi 
if [ -e $SLURM_SUBMIT_DIR/FCMINT       ]; then cp $SLURM_SUBMIT_DIR/FCMINT       $TMPDIR/FCMINT       ; fi 

# Change into scratch directory
cd $TMPDIR

# Run CFOUR 
% if background == 'yes':
$CFOUREXE >& $SLURM_SUBMIT_DIR/${output} &
$CFOURXJA &
% else:
$CFOUREXE >& $SLURM_SUBMIT_DIR/${output} 
$CFOURXJA
% endif

# Place other useful job info in a separate directory 
mkdir -p $SLURM_SUBMIT_DIR/Job_Data
cp $TMPDIR/den.dat  $SLURM_SUBMIT_DIR/Job_Data/den.dat 
cp $TMPDIR/FCMINT   $SLURM_SUBMIT_DIR/Job_Data/FCMINT
cp $TMPDIR/FCMFINAL $SLURM_SUBMIT_DIR/Job_Data/FCMFINAL 
cp $TMPDIR/JOBARC   $SLURM_SUBMIT_DIR/Job_Data/JOBARC
cp $TMPDIR/JAINDX   $SLURM_SUBMIT_DIR/Job_Data/JAINDX 
cp $TMPDIR/MOLDEN   $SLURM_SUBMIT_DIR/Job_Data/MOLDEN 
cp $TMPDIR/ZMATnew  $SLURM_SUBMIT_DIR/ZMATnew 
if [ -e "$TMPDIR/zmat001"  ]; then mkdir $SLURM_SUBMIT_DIR/Disps ; cp $TMPDIR/zmat* $SLURM_SUBMIT_DIR/Disps ; fi
if [ -e "$TMPDIR/FJOBARC"  ]; then cp $TMPDIR/FJOBARC $SLURM_SUBMIT_DIR/Job_Data/FJOBARC                    ; fi

# Go back to working directory
cd $SLURM_SUBMIT_DIR


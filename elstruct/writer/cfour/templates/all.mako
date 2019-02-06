MOLECULE PART 1/COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
${comment}
${geom}
----------------------------

JOB TYPE BLOCKS (CHOOSE ONE)
++++++++++++++++++++++++++++
*CFOUR(

ENERGY BLOCK 
----------------------------
GEO_METHOD=SINGLE_POINT
VIBRATION=0
----------------------------

OPTIMIZATION BLOCK 
----------------------------
GEO_METHOD=NR
VIBRATION=0
----------------------------

TS OPTIMIZATION BLOCK 
----------------------------
GEO_METHOD=TS
VIBRATION=0
----------------------------

HARM FREQUENCY ANALYT  BLOCK 
----------------------------
GEO_METHOD=SINGLE_POINT
VIBRATION=ANALYTIC
----------------------------

HARM FREQUENCY FINDIF  BLOCK 
----------------------------
GEO_METHOD=SINGLE_POINT
VIBRATION=FINDIF
----------------------------

++++++++++++++++++++++++++++

THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
CALC_LEVEL=${method}
REFERENCE=${reference}
BASIS=${basis}
----------------------------

MOLECULE BLOCK (REQUIRED) 
----------------------------
CHARGE=${charge}
MULTIPLICITY=${mult}
----------------------------

COORD_SYS BLOCK 
----------------------------
COORDS=${coord_type}
UNITS=${units}
----------------------------

MEMORY/SPECIAL OPTIONS BLOCK
---------------------------
MEMORY_SIZE=${memory}
% if special_ops == False:
MEM_UNIT=GB)

% else
${special}
MEM_UNIT=GB)

% endif


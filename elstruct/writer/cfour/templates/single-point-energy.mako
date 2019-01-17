${comment}
${geom}

*CFOUR(GEO_METHOD=SINGLE_POINT
VIBRATION=0
CALC_LEVEL=${method}
REFERENCE=${reference}
BASIS=${basis}
CHARGE=${charge}
MULTIPLICITY=${mult}
COORDS=${coord_type}
UNITS=${units}
MEMORY_SIZE=${memory}
% if special_ops == False:
MEM_UNIT=GB)

% else
${special}
MEM_UNIT=GB)

% endif


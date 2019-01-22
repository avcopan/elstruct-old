***,${comment}

memory,${memory},m

angstrom
geometry = {
${geom}
}

set,spin=${spin}
set,charge=${charge}

basis=${basis}

{${scf_method}}
% if corr_method != 'none':
{${corr_method}}
% endif
{optg}
{freq}

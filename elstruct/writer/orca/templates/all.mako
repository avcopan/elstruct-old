
MEMORY/COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
# ${comment}

% pal nprocs ${nprocs} end
% MaxCore ${memory} 
----------------------------


THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
% if ${corr_method} is NotEmpty:
! ${scf_method}
% else
if ${corr_method} is NotEmpty:
! ${scf_method} ${corr_method}
% endif 
! ${basis}

%scf
${scf_options}
end

% if ${corr_method} is MP2:
%mp2
${corr_options}
end
% endif

% if ${corr_method} is CC:
%mdci
${corr_options}
end
% endif

----------------------------

JOB TYPE BLOCKS (CHOOSE ONE OR MORE)
++++++++++++++++++++++++++++


OPTIMIZATION BLOCK 
----------------------------



++++++++++++++++++++++++++++

MOLECULE BLOCK (REQUIRED)
----------------------------
* ${coord_sys} ${charge} ${mult}
${geom}
*
----------------------------


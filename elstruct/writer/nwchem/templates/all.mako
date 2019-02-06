COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
start ${start_title}
title "${comment}"

echo
----------------------------

SCRATCH SET BLOCK (REQUIRED?)
----------------------------
scratch_dir ${scratch_dir}
----------------------------

MEMORY BLOCK (STRONGLY RECOMMENDED)
----------------------------
memory stack ${memory_stack} mb heap ${memory_heap} mb ${memory_global} 10000 mb noverify
----------------------------

MOLECULE BLOCK (REQUIRED)
----------------------------
geometry units angstrom
${geom}
Q: how to set charge and spin
----------------------------

THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
basis
  all library ${basis}
end

task scf
----------------------------

JOB TYPE BLOCKS (CHOOSE ONE OR MORE)
++++++++++++++++++++++++++++
++++++++++++++++++++++++++++


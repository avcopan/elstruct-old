start ${start_title}
title "${comment}"

echo

scratch_dir ${scratch_dir}

memory stack ${memory_stack} mb heap ${memory_heap} mb ${memory_global} 10000 mb noverify

geometry units angstrom
${geom}

basis
  all library ${basis}
end

task scf



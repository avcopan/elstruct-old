'''
  Set of functions to write large scale batches of jobs. Functions included below:
      grab_structures   : parses the structure file from ANL paper and returns info needed to write jobs
      set_build_options :
      write_input_file  :  
'''

import os
from mako.template import Template

def grab_structures(infilename):

  # Read in the structures from the desired structure file
  with open(infilename,'r') as inputfile:
    data = inputfile.readlines() 

  # Get the lines for each structure
  mult_lines = []
  for i in range(len(data)):
    if 'mult' in data[i]:
      mult_lines.append(int(i))

  # Get the names, multiplicities and structures
  names = []
  mults = []
  coords = []
  for linenum in mult_lines:
    names.append(data[linenum-1].strip())
    mults.append(int(data[linenum].strip().split()[1]))
    for j in range(linenum,linenum+100):
      if data[j].strip() == '':
        struct_end = j - 1
        break
    coords.append( [ data[k] for k in range(linenum+1,struct_end+1) ] )

  return names, mults, coords

def write_input_file(name, mult, coords, template_name, augbasis, densityfit): 

  # Obtain the path to the directory containing the templates
  DIR_PATH = os.path.dirname(os.path.realpath(__file__))
  TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

  # Obtain the name of the template corresponding to the requested electronic structure job
  template_file_path = os.path.join(TEMPLATE_PATH, template_name)

  # Get coords in string
  xyz_str = ''
  for line in coords:
    xyz_str = xyz_str + line        
  xyz_str = xyz_str[:-1]

  # Dict ot pass in values
  fill_vals = {
    'name' : name,
    'mult' : mult,
    'coords' : xyz_str,
    'augbasis' : augbasis,
    'densityfit' : densityfit
  }

  # Create template object with the user-requested options
  substituted_template = Template(filename=template_file_path).render(**fill_vals)

  # Write inputfile
  with open('input.dat',"w") as inputfile:
    inputfile.write(substituted_template)


  return None

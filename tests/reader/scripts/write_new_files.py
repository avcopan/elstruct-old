"""
Script to generate new files from a simple RHF/UHF/ROHF files
"""

__authors__ = "Kevin Moore"
__updated__ = "2019-01-20"

import os
from changes import OLD_LINES_ORCA
from changes import NEW_LINES_ORCA


# Reset dicts cuz I am lazy
OLD_LINES = OLD_LINES_ORCA
NEW_LINES = NEW_LINES_ORCA
PROGRAM = 'orca'
OVERWRITE = False

# Get path
# DATA_PATH = os.path.dirname(os.path.realpath(__file__), '../data/', PROGRAM)
DATA_PATH = os.getcwd()

# Loop through each input file and run the file
for ref in ('rhf', 'uhf', 'rohf'):

    # Loop through all the desired changes
    for i in range(len(NEW_LINES[ref])):

        # Set the old file name and new file name
        old_file_path = os.path.join(DATA_PATH, OLD_LINES[ref][1])
        new_file_path = os.path.join(DATA_PATH, NEW_LINES[ref][i][1])
        old_file_name = old_file_path + '/input.dat'
        new_file_name = new_file_path + '/input.dat'

        # Set the old method string and new method string
        old_file_str = OLD_LINES[ref][0]
        new_file_str = NEW_LINES[ref][i][0]

        # Empty list of lines for the loop
        old_file_lines = []
        new_file_lines = []

        # Make the new directory
        if os.path.exists(new_file_path) is False:
            os.mkdir(new_file_path)

        # Read the contents of the original file
        with open(old_file_name, 'r') as old_file:
            old_file_lines = old_file.readlines()

        # Loop through of original file building a list of lines for new file
        for line in old_file_lines:
            # If line to change (line1) in loop, add altered line (line2)
            if old_file_str in line:
                new_file_lines.append(new_file_str)
            # Otherwise just add the current line
            else:
                new_file_lines.append(line)

        # Write new file with the new lines (including the line change)
        if os.path.exists(new_file_name) is False or \
           os.path.exists(new_file_name) is True and OVERWRITE is True:
            with open(new_file_name, 'w') as new_file:
                for line in new_file_lines:
                    new_file.writelines(line)

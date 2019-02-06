""" temporary script
"""
from elstruct import reader

with open('molpro_output.dat') as output_file:
    OUTPUT_STRING = output_file.read()

print(reader.optimized_internal_geometry(prog='molpro2015', output_string=OUTPUT_STRING))

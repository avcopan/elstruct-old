""" install elstruct
"""
from distutils.core import setup


setup(name="elstruct",
      version="0.1.0",
      packages=["elstruct",
                "elstruct.writer",
                "elstruct.writer.psi4",
                "elstruct.writer.molpro",
                "elstruct.runner",
                "elstruct.runner.bebop",
                "elstruct.runner.blues",
                "elstruct.reader",
                "elstruct.reader.psi4",
                "elstruct.reader.molpro",
                "elstruct.reader.rere"],
      package_dir={'elstruct': 'elstruct'},
      package_data={'elstruct': [
          'writer/psi4/templates/*.mako', 
          'writer/molpro/templates/*.mako', 
          'runner/blues/templates/*.mako',
          'runner/bebop/templates/*.mako',
          ]
      },
      scripts=["scripts/sblues"])

""" .xyz-based functions
"""
import re
from .reader.rere.pattern_lib import WHITESPACE
from .reader.rere.pattern_lib import UNSIGNED_INTEGER
from .reader.rere.pattern_lib import STRING_START
from .reader.rere.pattern_lib import LINE_END
from .reader.rere.pattern_lib import LETTER
from .reader.rere.pattern_lib import FLOAT
from .reader.rere.pattern import maybe
from .reader.rere.pattern import one_or_more
from .reader.rere.pattern import named_capturing

WHITESPACES = one_or_more(WHITESPACE)


def number_of_atoms(dxyz):
    """ number of atoms from a .xyz string
    """
    natms_pattern = maybe(WHITESPACES).join(
        [STRING_START, named_capturing(UNSIGNED_INTEGER, 'natms'), LINE_END])
    match = re.search(natms_pattern, dxyz, re.MULTILINE)
    assert match
    gdct = match.groupdict()
    natms = int(gdct['natms'])
    return natms


def to_geometry(dxyz):
    """ cartesian geometry from a .xyz string
    """
    natms = number_of_atoms(dxyz)
    atomic_symbol = LETTER + maybe(LETTER)
    atom_pattern = WHITESPACES.join(
        [named_capturing(atomic_symbol, 'asymb'), named_capturing(FLOAT, 'x'),
         named_capturing(FLOAT, 'y'), named_capturing(FLOAT, 'z')])
    line_pattern = atom_pattern + maybe(WHITESPACES) + LINE_END

    cart_geom = []
    for match in re.finditer(line_pattern, dxyz, re.MULTILINE):
        gdct = match.groupdict()
        asymb = gdct['asymb']
        xyz = tuple(map(float, [gdct['x'], gdct['y'], gdct['z']]))
        cart_geom.append((asymb, xyz))

    if len(cart_geom) != natms:
        raise ValueError("\nThis .xyz file is inconsistent: {:s}".format(dxyz))

    return tuple(cart_geom)


def from_geometry(cart_geom):
    """ .xyz string from a cartesian geometry
    """
    natms = len(cart_geom)
    dxyz = '{:d}\n\n'.format(natms)
    for (asymb, xyz) in cart_geom:
        dxyz += '{:s} {:s} {:s} {:s}\n'.format(asymb, *map(repr, xyz))
    return dxyz

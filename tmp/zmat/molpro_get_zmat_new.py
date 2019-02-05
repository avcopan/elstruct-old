""" temporary script 3
"""
import numpy
import elstruct
import elstruct.reader.rere.find as ref
import elstruct.reader.rere.pattern as rep
import elstruct.reader.rere.pattern_lib as relib

SPACE = relib.NONNEWLINE_WHITESPACE
MAYBE_SPACES = rep.zero_or_more(SPACE)
ATOM_KEY_PATTERN = (relib.LETTER + rep.maybe(relib.LETTER) +
                    rep.maybe(relib.UNSIGNED_INTEGER))
ATOM_INDEX_PATTERN = relib.UNSIGNED_INTEGER
COORD_KEY_PATTERN = relib.LETTER + rep.zero_or_more(relib.NONWHITESPACE)
COORD_VAL_PATTERN = relib.FLOAT

ATOM_ID_PATTERN = rep.one_of_these([ATOM_KEY_PATTERN, ATOM_INDEX_PATTERN])
COORD_ID_PATTERN = rep.one_of_these([COORD_VAL_PATTERN, COORD_KEY_PATTERN])

ZMAT_LINE_PATTERNS = [
    MAYBE_SPACES.join([
        relib.LINE_START, ATOM_KEY_PATTERN, relib.LINE_END]),
    MAYBE_SPACES.join([
        relib.LINE_START, ATOM_KEY_PATTERN, SPACE,
        ATOM_ID_PATTERN, SPACE, COORD_ID_PATTERN, relib.LINE_END]),
    MAYBE_SPACES.join([
        relib.LINE_START, ATOM_KEY_PATTERN, SPACE,
        ATOM_ID_PATTERN, SPACE, COORD_ID_PATTERN, SPACE,
        ATOM_ID_PATTERN, SPACE, COORD_ID_PATTERN, relib.LINE_END]),
    MAYBE_SPACES.join([
        relib.LINE_START, ATOM_KEY_PATTERN, SPACE,
        ATOM_ID_PATTERN, SPACE, COORD_ID_PATTERN, SPACE,
        ATOM_ID_PATTERN, SPACE, COORD_ID_PATTERN, SPACE,
        ATOM_ID_PATTERN, SPACE, COORD_ID_PATTERN, relib.LINE_END])
]

ZMAT_PATTERN1 = ZMAT_LINE_PATTERNS[0]
ZMAT_PATTERN2 = relib.NEWLINE.join(ZMAT_LINE_PATTERNS[:2])
ZMAT_PATTERN3 = (
    relib.NEWLINE.join(ZMAT_LINE_PATTERNS[:3]) +
    rep.zero_or_more(relib.NEWLINE + ZMAT_LINE_PATTERNS[3])
)

ZMAT_PATTERN = rep.one_of_these([ZMAT_PATTERN3, ZMAT_PATTERN2, ZMAT_PATTERN1])

ATOM_KEY_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN)
])
BOND_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN), SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, rep.capturing(COORD_ID_PATTERN)
])
ANGLE_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN), SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, COORD_ID_PATTERN, SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, rep.capturing(COORD_ID_PATTERN)
])
TORSION_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN), SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, COORD_ID_PATTERN, SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, COORD_ID_PATTERN, SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, rep.capturing(COORD_ID_PATTERN)
])


def zmatrix_coordinate_definitions(output_string):
    """ get the zmatrix coordinates from the output file
    """
    zmat_str = ref.first_capture(rep.capturing(ZMAT_PATTERN), output_string)
    atom_keys = ref.all_captures(ATOM_KEY_CAPTURING_PATTERN, zmat_str)
    bond_caps_lst = ref.all_captures(BOND_CAPTURING_PATTERN, zmat_str)
    angle_caps_lst = ref.all_captures(ANGLE_CAPTURING_PATTERN, zmat_str)
    torsion_caps_lst = ref.all_captures(TORSION_CAPTURING_PATTERN, zmat_str)

    dummy_atom_indices = [i for i, atom_key in enumerate(atom_keys)
                          if atom_key.upper().startswith('X')]

    atom_id2index = {}
    atom_id2index.update(
        {atom_key: idx for idx, atom_key in enumerate(atom_keys)})
    atom_id2index.update(
        {str(idx+1): idx for idx, _ in enumerate(atom_keys)})

    coord_caps_lst = bond_caps_lst + angle_caps_lst + torsion_caps_lst
    zmat_coord_dct = {
        tuple(map(atom_id2index.__getitem__, caps[:-1])): caps[-1]
        for caps in coord_caps_lst}

    dummy_atom_dct = {
        coord[0]: coord[1:]
        for coord in zmat_coord_dct
        if coord[0] in dummy_atom_indices and len(coord) == 4
    }
    return zmat_coord_dct, dummy_atom_dct


def zmat_coordinate_initial_values(output_string, zmat_coord_dct):
    """ initial zmatrix values
    """
    zmat_coord_val_dct = {}
    for coord_def, coord_key in zmat_coord_dct.items():
        coord_val_pattern = MAYBE_SPACES.join([
            relib.LINE_START, 'SETTING', coord_key.upper(), '=',
            rep.capturing(relib.FLOAT)
        ])
        coord_val_str = ref.first_capture(coord_val_pattern, output_string)
        assert coord_val_str is not None
        zmat_coord_val_dct[coord_def] = float(coord_val_str)
    return zmat_coord_val_dct


# zmat -> xyz conversion
def unit_norm(xyz):
    """ vector normalized to 1
    """
    norm = numpy.linalg.norm(xyz)
    uxyz = numpy.divide(xyz, norm)
    assert numpy.allclose(numpy.linalg.norm(uxyz), 1.)
    return uxyz


def unit_direction(xyz1, xyz2):
    """ calculate a unit direction vector from `xyz1` to `xyz2`
    """
    dxyz12 = numpy.subtract(xyz2, xyz1)
    uxyz12 = unit_norm(dxyz12)
    return uxyz12


def unit_perpendicular(xyz1, xyz2):
    """ calculate a unit perpendicular on `xyz1` and `xyz2`
    """
    xyz3 = numpy.cross(xyz1, xyz2)
    uxyz3 = unit_norm(xyz3)
    return uxyz3


def local_axes(xyz1, xyz2, xyz3):
    """ local axes for defining bond, angle, torsion from support atoms
    """
    uxyz12 = unit_direction(xyz1, xyz2)
    uxyz23 = unit_direction(xyz2, xyz3)
    uxyz123_perp = unit_perpendicular(uxyz12, uxyz23)

    z_ax = tuple(uxyz12)
    y_ax = tuple(unit_perpendicular(uxyz123_perp, z_ax))
    x_ax = tuple(unit_perpendicular(y_ax, z_ax))
    return (x_ax, y_ax, z_ax)


def local_position(dist, ang, tors):
    """ position by internal coordinates in the local axis frame
    """
    x_comp = dist * numpy.sin(ang) * numpy.sin(tors)
    y_comp = dist * numpy.sin(ang) * numpy.cos(tors)
    z_comp = dist * numpy.cos(ang)
    return (x_comp, y_comp, z_comp)


def insert_dummy_atoms(geo, dummy_atom_dct, zmat_val_dct):
    """ insert dummy atoms into the geometry
    """
    deg2rad = numpy.pi / 180.

    symbols, xyzs = zip(*geo)
    symbols = list(symbols)
    xyzs = list(xyzs)
    for dummy_atom_idx, support_atom_idxs in sorted(dummy_atom_dct.items()):
        sidx1, sidx2, sidx3 = support_atom_idxs
        sxyz1, sxyz2, sxyz3 = map(xyzs.__getitem__, support_atom_idxs)
        dist = zmat_val_dct[(dummy_atom_idx, sidx1)]
        ang = zmat_val_dct[(dummy_atom_idx, sidx1, sidx2)]
        tors = zmat_val_dct[(dummy_atom_idx, sidx1, sidx2, sidx3)]
        local_xyz = local_position(dist, ang * deg2rad, tors * deg2rad)
        axes = local_axes(sxyz1, sxyz2, sxyz3)
        dummy_atom_xyz = tuple(numpy.add(sxyz1, numpy.dot(local_xyz, axes)))
        symbols.insert(dummy_atom_idx, 'X')
        xyzs.insert(dummy_atom_idx, dummy_atom_xyz)

    assert len(symbols) == len(xyzs)
    geo = tuple(zip(symbols, xyzs))
    return geo


def bond_distance(geo, idx1, idx2):
    """ bond distance
    """
    _, xyzs = zip(*geo)
    xyz1, xyz2 = map(xyzs.__getitem__, (idx1, idx2))
    dxyz12 = numpy.subtract(xyz2, xyz1)
    dist12 = numpy.linalg.norm(dxyz12)
    return dist12


def bond_angle(geo, idx1, idx2, idx3):
    """ bond angle
    """
    _, xyzs = zip(*geo)
    xyz1, xyz2, xyz3 = map(xyzs.__getitem__, (idx1, idx2, idx3))
    uxyz21 = unit_direction(xyz2, xyz1)
    uxyz23 = unit_direction(xyz2, xyz3)
    ang = numpy.arccos(numpy.dot(uxyz21, uxyz23))
    return ang * 180. / numpy.pi


def torsion_angle(geo, idx1, idx2, idx3, idx4):
    """ torsion angle
    """
    _, xyzs = zip(*geo)
    xyz1, xyz2, xyz3, xyz4 = map(xyzs.__getitem__, (idx1, idx2, idx3, idx4))
    uxyz21 = unit_direction(xyz2, xyz1)
    uxyz23 = unit_direction(xyz2, xyz3)
    uxyz32 = unit_direction(xyz3, xyz2)
    uxyz34 = unit_direction(xyz3, xyz4)
    uxyz123_perp = unit_perpendicular(uxyz21, uxyz23)
    uxyz234_perp = unit_perpendicular(uxyz32, uxyz34)
    tors = numpy.arccos(numpy.dot(uxyz123_perp, uxyz234_perp))
    return tors * 180. / numpy.pi


if __name__ == '__main__':
    with open('molpro_output.dat') as output_file:
        OUTPUT_STRING = output_file.read()

    ZMAT_COORD_DCT, DUMMY_ATOM_DCT = zmatrix_coordinate_definitions(
        OUTPUT_STRING)
    print(ZMAT_COORD_DCT)

    ZMAT_COORD_VAL_DCT = zmat_coordinate_initial_values(OUTPUT_STRING,
                                                        ZMAT_COORD_DCT)
    print(ZMAT_COORD_VAL_DCT)

    GEO = elstruct.reader.optimized_cartesian_geometry(
        'molpro2015', OUTPUT_STRING)
    print(GEO)

    GEO_WITH_DUMMIES = insert_dummy_atoms(
        GEO, DUMMY_ATOM_DCT, ZMAT_COORD_VAL_DCT)

    for coord, key in ZMAT_COORD_DCT.items():
        print(coord, key)
        if len(coord) == 2:
            print(bond_distance(GEO_WITH_DUMMIES, *coord))
        if len(coord) == 3:
            print(bond_angle(GEO_WITH_DUMMIES, *coord))
        if len(coord) == 4:
            print(torsion_angle(GEO_WITH_DUMMIES, *coord))

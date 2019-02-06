""" Z-Matrix helpers
"""
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib

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
BOND_DISTANCE_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN), SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, rep.capturing(COORD_ID_PATTERN)
])
BOND_ANGLE_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN), SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, COORD_ID_PATTERN, SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, rep.capturing(COORD_ID_PATTERN)
])
TORSION_ANGLE_CAPTURING_PATTERN = MAYBE_SPACES.join([
    relib.LINE_START, rep.capturing(ATOM_KEY_PATTERN), SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, COORD_ID_PATTERN, SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, COORD_ID_PATTERN, SPACE,
    rep.capturing(ATOM_ID_PATTERN), SPACE, rep.capturing(COORD_ID_PATTERN)
])


def first_zmatrix_string(output_str):
    """ get the first zmatrix in the output string
    """
    zmat_str = ref.first_capture(rep.capturing(ZMAT_PATTERN), output_str)
    return zmat_str


def zmatrix_dummy_atom_support_indices(output_str):
    """ indices of dummy atoms and their "supporting atoms"

    "supporting atoms" = atoms defining the dummy atom's torsion angle
    (assumes all dummy atoms have torsion angles)
    """
    zmat_str = first_zmatrix_string(output_str)

    tors_keys = list(torsion_angle_entries(zmat_str).keys())
    dummy_idxs = [i for i, atm_lbl in enumerate(atom_labels(zmat_str))
                  if atm_lbl.upper().startswith('X')
                  or atm_lbl.upper().startswith('Q')]
    dummy_sidx_dct = {
        tors_key[0]: tors_key[1:] for tors_key in tors_keys
        if tors_key[0] in dummy_idxs}

    assert len(dummy_idxs) == len(dummy_sidx_dct)
    return dummy_sidx_dct


def internal_coordinate_entries(zmat_str):
    """ get the entries of the internal coordinates as a dictionary
    """
    intco_entry_dct = {}
    intco_entry_dct.update(bond_distance_entries(zmat_str))
    intco_entry_dct.update(bond_angle_entries(zmat_str))
    intco_entry_dct.update(torsion_angle_entries(zmat_str))
    return intco_entry_dct


def bond_distance_entries(zmat_str):
    """ bond distance entries
    """
    atm_idx_dct = _atom_index_mapping(zmat_str)
    dist_caps_lst = ref.all_captures(BOND_DISTANCE_CAPTURING_PATTERN, zmat_str)
    dist_entry_dct = {tuple(map(atm_idx_dct.__getitem__, caps[:-1])): caps[-1]
                      for caps in dist_caps_lst}
    return dist_entry_dct


def bond_angle_entries(zmat_str):
    """ bond angle entries
    """
    atm_idx_dct = _atom_index_mapping(zmat_str)
    ang_caps_lst = ref.all_captures(BOND_ANGLE_CAPTURING_PATTERN, zmat_str)
    ang_entry_dct = {tuple(map(atm_idx_dct.__getitem__, caps[:-1])): caps[-1]
                     for caps in ang_caps_lst}
    return ang_entry_dct


def torsion_angle_entries(zmat_str):
    """ torsion angle entries
    """
    atm_idx_dct = _atom_index_mapping(zmat_str)
    tors_caps_lst = ref.all_captures(TORSION_ANGLE_CAPTURING_PATTERN, zmat_str)
    tors_entry_dct = {tuple(map(atm_idx_dct.__getitem__, caps[:-1])): caps[-1]
                      for caps in tors_caps_lst}
    return tors_entry_dct


def atom_labels(zmat_str):
    """ z-matrix atom labels
    """
    return ref.all_captures(ATOM_KEY_CAPTURING_PATTERN, zmat_str)


def _atom_index_mapping(zmat_str):
    atm_entries = atom_labels(zmat_str)
    atm_idxs = tuple(range(len(atm_entries)))
    atm_one_idx_strs = [str(atm_idx+1) for atm_idx in atm_idxs]
    atm_idx_dct = dict(zip(atm_entries, atm_idxs))
    atm_idx_dct.update(dict(zip(atm_one_idx_strs, atm_idxs)))
    return atm_idx_dct

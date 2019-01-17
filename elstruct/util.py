""" common writer utilities
"""


def xyz_string(labels, coords):
    """ .xyz format string for this cartesian geometry
    :param labels: optional labels for the beginnings of atom lines, by index
    :type labels: dict
    """
    assert len(labels) == len(coords)
    dxyz = '\n'.join(
        '{:s} {:s} {:s} {:s}'.format(asymb, *map(repr, xyz))
        for asymb, xyz in zip(labels, coords))
    return dxyz

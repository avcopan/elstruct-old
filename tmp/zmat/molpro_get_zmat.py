""" temporary script 2
"""
import elstruct.reader.rere.find as ref
import elstruct.reader.rere.pattern as rep
import elstruct.reader.rere.pattern_lib as relib

MAYBE_SPACES = rep.zero_or_more(relib.NONNEWLINE_WHITESPACE)
VAR_NAME_PATTERN = relib.LETTER + rep.zero_or_more(relib.NONWHITESPACE)


def zmatrix_reader(output_string):
    """ read the zmatrix from the output
    """
    zmat_def_dct = _zmat_variable_definitions(output_string)
    zmat_val_dct = {}
    for var_key in zmat_def_dct.keys():
        var_val_pattern = MAYBE_SPACES.join([
            relib.LINE_START, 'SETTING', var_key, '=',
            rep.capturing(relib.FLOAT)
        ])
        var_val = ref.first_capture(var_val_pattern, output_string)
        assert var_val is not None
        zmat_val_dct[var_key] = float(var_val)

    return zmat_def_dct, zmat_val_dct


def _geometry_section(output_string):
    geometry_word = '[Gg][Ee][Oo][Mm][Ee][Tt][Rr][Yy]'
    start_pattern = MAYBE_SPACES.join([
        geometry_word, rep.escape('='), rep.escape('{')])
    body_pattern = rep.one_or_more(relib.ANY_CHAR, greedy=False)
    end_pattern = rep.escape('}')
    section_pattern = MAYBE_SPACES.join([
        start_pattern, rep.capturing(body_pattern), end_pattern])
    geom_section = ref.first_capture(section_pattern, output_string)
    return geom_section


def _line_start_variables(geom_section):
    start_var_pattern = MAYBE_SPACES.join([
        relib.LINE_START, rep.capturing(VAR_NAME_PATTERN)])
    start_vars = ref.all_captures(start_var_pattern, geom_section)
    return start_vars


def _potential_atom_key_and_identifier_patterns(string):
    possible_atom_keys = list(
        reversed(sorted(_line_start_variables(string), key=len)))
    possible_atom_number_strings = list(
        map(str, range(len(possible_atom_keys), 0, -1)))

    # these have been sorted to avoid sub-captures
    atom_key_pattern = rep.one_of_these(possible_atom_keys)
    atom_id_pattern = rep.one_of_these(possible_atom_keys +
                                       possible_atom_number_strings)
    return atom_key_pattern, atom_id_pattern


def _zmat_string(output_string):
    geom_section = _geometry_section(output_string)

    atom_key_pattern, atom_id_pattern = (
        _potential_atom_key_and_identifier_patterns(geom_section)
    )

    def _line_pattern(nvars):
        elements = [relib.LINE_START, atom_key_pattern]
        for _ in range(nvars):
            elements += [relib.NONNEWLINE_WHITESPACE, atom_id_pattern,
                         relib.NONNEWLINE_WHITESPACE, VAR_NAME_PATTERN]
        elements += [relib.LINE_END]
        pattern = MAYBE_SPACES.join(elements)
        return pattern

    def _lines_pattern(natms):
        parts = [_line_pattern(nvars=0)]
        if natms > 1:
            parts.append(_line_pattern(nvars=1))
        if natms > 2:
            parts.append(_line_pattern(nvars=2))
        if natms > 3:
            parts.append(
                rep.zero_or_more(_line_pattern(nvars=3) + relib.NEWLINE) +
                _line_pattern(nvars=3)
            )
        pattern = relib.NEWLINE.join(parts)
        return pattern

    zmat_pattern = rep.one_of_these(
        [_lines_pattern(natms=4), _lines_pattern(natms=3),
         _lines_pattern(natms=2), _lines_pattern(natms=1)])

    zmat_string = ref.last_capture(zmat_pattern, geom_section)
    return zmat_string


def _zmat_variable_definitions(output_string):
    zmat_string = _zmat_string(output_string)
    atom_key_pattern, atom_id_pattern = (
        _potential_atom_key_and_identifier_patterns(zmat_string)
    )

    key_pattern = MAYBE_SPACES.join([
        relib.LINE_START, rep.capturing(atom_key_pattern)
    ])
    bond_pattern = MAYBE_SPACES.join([
        relib.LINE_START, rep.capturing(atom_key_pattern),
        relib.NONNEWLINE_WHITESPACE,
        rep.capturing(atom_id_pattern), relib.NONNEWLINE_WHITESPACE,
        rep.capturing(VAR_NAME_PATTERN)
    ])
    angle_pattern = MAYBE_SPACES.join([
        relib.LINE_START, rep.capturing(atom_key_pattern),
        relib.NONNEWLINE_WHITESPACE,
        rep.capturing(atom_id_pattern), relib.NONNEWLINE_WHITESPACE,
        VAR_NAME_PATTERN, relib.NONNEWLINE_WHITESPACE,
        rep.capturing(atom_id_pattern), relib.NONNEWLINE_WHITESPACE,
        rep.capturing(VAR_NAME_PATTERN)
    ])
    torsion_pattern = MAYBE_SPACES.join([
        relib.LINE_START, rep.capturing(atom_key_pattern),
        relib.NONNEWLINE_WHITESPACE,
        rep.capturing(atom_id_pattern), relib.NONNEWLINE_WHITESPACE,
        VAR_NAME_PATTERN, relib.NONNEWLINE_WHITESPACE,
        rep.capturing(atom_id_pattern), relib.NONNEWLINE_WHITESPACE,
        VAR_NAME_PATTERN, relib.NONNEWLINE_WHITESPACE,
        rep.capturing(atom_id_pattern), relib.NONNEWLINE_WHITESPACE,
        rep.capturing(VAR_NAME_PATTERN)
    ])
    keys = ref.all_captures(key_pattern, zmat_string)
    bond_caps_lst = ref.all_captures(bond_pattern, zmat_string)
    angle_caps_lst = ref.all_captures(angle_pattern, zmat_string)
    torsion_caps_lst = ref.all_captures(torsion_pattern, zmat_string)

    nums = list(map(str, range(1, len(keys)+1)))

    # dictionary mapping atom ids to numerical indices
    index_dct = dict(map(reversed, enumerate(keys)))
    index_dct.update(dict(map(reversed, enumerate(nums))))

    def _split_last(seq_lst):
        last_lst = [seq[-1] for seq in seq_lst]
        others_lst = [seq[:-1] for seq in seq_lst]
        return last_lst, others_lst

    bond_keys, bond_defs_lst = _split_last(bond_caps_lst)
    angle_keys, angle_defs_lst = _split_last(angle_caps_lst)
    torsion_keys, torsion_defs_lst = _split_last(torsion_caps_lst)

    bond_keys = tuple(map(str.upper, bond_keys))
    angle_keys = tuple(map(str.upper, angle_keys))
    torsion_keys = tuple(map(str.upper, torsion_keys))

    bond_defs_lst = tuple(tuple(index_dct[atom_id] for atom_id in defs)
                          for defs in bond_defs_lst)
    angle_defs_lst = tuple(tuple(index_dct[atom_id] for atom_id in defs)
                           for defs in angle_defs_lst)
    torsion_defs_lst = tuple(tuple(index_dct[atom_id] for atom_id in defs)
                             for defs in torsion_defs_lst)

    zmat_def_dct = {}
    zmat_def_dct.update(dict(zip(bond_keys, bond_defs_lst)))
    zmat_def_dct.update(dict(zip(angle_keys, angle_defs_lst)))
    zmat_def_dct.update(dict(zip(torsion_keys, torsion_defs_lst)))

    return zmat_def_dct


if __name__ == '__main__':
    with open('molpro_output.dat') as output_file:
        OUTPUT_STRING = output_file.read()

    print(zmatrix_reader(OUTPUT_STRING))

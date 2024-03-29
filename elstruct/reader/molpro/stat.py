"""
Library of functions to assess the job status of a Molpro 2018 job
from the output file.

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import find as ref


# Series of functions to read job status information

def error_msg_reader(output_string):
    """ Searches the output file for possible error messages.
    """

    # List of possible strings denoting error messages in the output file
    error_msg_patterns = [
        # Printed when SCF, CC, iterations fail to converge
        '',
        # Printed when geom. opt fails to converge
        'No convergence in max. number of iterations'
    ]

    # Initialize error_msg to empty string; replaced if error is found
    error_msg = ''

    # Check for all of the error pattern strings
    for pattern in error_msg_patterns:
        check_error = ref.has_match(pattern, output_string)
        if check_error:
            error_msg = pattern

    return error_msg


def complete_msg_reader(output_string):
    """ Checks if the job completes successfully.
        Returns job status and any error messages located
    """

    # Line printed if Molpro exits normally
    complete_msg_pattern = 'Variable memory released'

    # Check if the job went to completion
    complete_status = ref.has_match(complete_msg_pattern, output_string)

    return complete_status

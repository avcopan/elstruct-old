"""
Library of functions to assess the job status of a MRCC 2018 job using the output file.

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read job status information #####

def error_msg_reader(output_string):
    """ Searches the output file for possible error messages.
    """

    # List of possible strings denoting error messages in the output file
    error_msg_patterns = [
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
    complete_msg_pattern = 'Normal termination of mrcc'

    # Check if the job went to completion
    complete_status = ref.has_match(complete_msg_pattern, output_string)

    return complete_status


##### Status reader function called by external scripts #####

def status(output_string):
    """ Returns the status of a job.
    """

    # Check if the job completed or if any error messages were printed
    job_complete = complete_msg_reader(output_string)
    job_error_str = error_msg_reader(output_string)

    job_status = [complete_status, job_error_str]

    return job_status

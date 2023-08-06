# # # # # # # # # # # # # # # # # # # # # # # # # #
# Formatting routines
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

def compactify (resources):
    """Improve format of 'resources' dictionary."""

    compact = ''
    for resource in resources:
        compact += '/' + resource ['owner'] + ('-' + str(resource ['address']) if resource ['address'] is not None else '')
    return compact if compact != '' else '/'

import re
# filter to remove special characters from strings to be used as filenames
def plain (name):
    """Filter to remove special characters from strings to be used as filenames."""

    return re.sub (r'\W+', '', name)

# WORK IN PROGRESS

import inspect

def assign (root, components):
    """Auto-magically assign all SPUX components to each other if possible."""

    argspec = inspect.getargspec (root.assign)
    del argspec
    # requirements = { 'root' : argspec.args }
    # names = [ component.name for component in components ]

    # recursive search
    # WORK IN PROGRESS

    return root
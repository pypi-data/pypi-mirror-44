# # # # # # # # # # # # # # # # # # # # # # # # # #
# Reporting
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from .format import compactify

def report (instance, method, extras = {}):
    ''' Report name, method, root, sandbox, and any specified extras provided verbosity is enabled.'''

    if not hasattr(instance,"verbosity"):
        return

    if instance.verbosity:
        root = (' root - ' + compactify (instance.root)) if hasattr (instance, 'root') else ''
        sandbox = ((', sandbox - %s' % instance.sandbox ()) if hasattr (instance, 'sandbox') else '') if instance.sandboxing else ''
        print (" :: %s model in '%s':%s%s" % (instance.name, method, root, sandbox))
        for key, extra in extras.items ():
            print ('  : -> %s' % key)
            print (extra)

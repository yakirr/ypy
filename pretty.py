from __future__ import print_function, division

def print_namespace(ns):
    for name, val in sorted(vars(ns).items()):
        if not name.startswith('_'):
            print('{:<25}{}'.format(name, val))

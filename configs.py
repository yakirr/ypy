from __future__ import print_function, division
import subprocess
import sys

def print_vars(ns):
    for name, val in sorted(vars(ns).items()):
        if not name.startswith('_'):
            print('{:<25}{}'.format(name, val))

def namespace_to_commandline(ns):
    return [x for name, val in sorted(vars(ns).items()) for x in ('--' + name, str(val))]

def bsub_command(command, outfilepath, jobname=None, queue='short', time_in_hours=12,
        cpus=12, memory_GB=8):
    return ['bsub'] + \
            (['-J', jobname] if jobname else []) + \
            ['-q', queue,
            '-W', str(time_in_hours) + ':00',
            '-oo', outfilepath,
            '-R', 'rusage[mem=' + str(memory_GB * 1024) + ',ncpus=' + str(cpus) + ']',
            ' '.join(command)]

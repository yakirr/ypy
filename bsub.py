from __future__ import print_function, division
import subprocess
import sys
import pretty

def add_main_and_submit(parser, main_function, submit_function):
    subparsers = parser.add_subparsers()

    subparser_main = subparsers.add_parser('main')
    subparser_main.set_defaults(_func=main_function)

    subparser_submit = subparsers.add_parser('submit')
    subparser_submit.set_defaults(_func=submit_function)

    return subparser_main, subparser_submit

def choose_parser_and_run(parser):
    args, _ = parser.parse_known_args()
    pretty.print_namespace(args); print()

    args._func(args)

def param_dict_to_commandline_list(d):
    result = []
    for k, v in d.items():
        result.append('--' + k)
        result.append(str(v))
    return result

def bsub_command(command, outfilepath, jobname=None, queue='short', time_in_hours=12,
        memory_GB=8):
    return ['bsub'] + \
        (['-J', jobname] if jobname else []) + \
        ['-q', queue,
        '-W', str(time_in_hours) + ':00',
        '-oo', outfilepath,
        '-R', '"rusage[mem=' + str(memory_GB * 1024) + '] select[model!=XeonE5345 && model!=XeonE5430]"',
        ' '.join(command)]

def submit(command, outfilepath, jobname=None, queue='short', time_in_hours=12, memory_GB=8,
        debug=False):
    bsub_cmd = bsub_command(command, outfilepath, jobname, queue, time_in_hours, memory_GB)
    print('\033[92m' + ' '.join(bsub_cmd) + '\033[0m')
    print('\033[94m' + outfilepath + '\033[0m')
    if not debug:
        subprocess.call(bsub_cmd)

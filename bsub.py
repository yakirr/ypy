from __future__ import print_function, division
import subprocess
import sys
import pretty

def add_main_and_submit(parser, main_function, submit_function,
        merge_function=None,
        main_parents=[],
        submit_parents=[],
        merge_parents=[]):
    subparsers = parser.add_subparsers()

    subparser_main = subparsers.add_parser('main', parents=main_parents)
    subparser_main.set_defaults(_func=main_function)

    subparser_submit = subparsers.add_parser('submit', parents=submit_parents)
    subparser_submit.set_defaults(_func=submit_function)

    if merge_function is None:
        return subparser_main, subparser_submit
    else:
        subparser_merge = subparsers.add_parser('merge', parents=merge_parents)
        subparser_merge.set_defaults(_func=merge_function)
        return subparser_main, subparser_submit, subparser_merge

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
        time_in_minutes=None, memory_GB=8, depends_on=None):
    if time_in_minutes:
        time = '0:' + str(time_in_minutes)
    else:
        time = str(time_in_hours) + ':00'
    return ['bsub'] + \
        (['-J', jobname] if jobname else []) + \
        ['-q', queue,
        '-W', time,
        '-oo', outfilepath,
        '-R', '"rusage[mem=' + str(int(memory_GB * 1024)) + \
                '] select[model!=XeonE5345 && model!=XeonE5430]"'] + \
            (['-w', 'done({})'.format(depends_on)] if depends_on is not None else []) + \
        [' '.join(command)]

def submit(command, outfilepath, jobname=None, queue='short', time_in_hours=12,
        time_in_minutes=None, memory_GB=8, depends_on=None, debug=False):
    bsub_cmd = bsub_command(command, outfilepath, jobname, queue,
            time_in_hours, time_in_minutes, memory_GB, depends_on)
    print('\033[92m' + ' '.join(bsub_cmd) + '\033[0m')
    print('\033[94m' + outfilepath + '\033[0m')
    if not debug:
        output = subprocess.check_output(bsub_cmd)
        print(output)
        return output.replace('[','<').replace('>','<').split('<')[1] # parse out job id
    else:
        return 'JOBID'

from __future__ import print_function, division
import subprocess
import math
import pretty

# produces an LSF-formatted bsub command
def bsub_command(command, outfilepath, jobname=None, queue='short', time_in_hours=12,
        time_in_minutes=None, memory_GB=8, depends_on=None):
    if time_in_minutes:
        time = '0:' + str(time_in_minutes)
    else:
        time = str(time_in_hours) + ':00'
    # the commented line below is to filter out ottavinos, but those should usually be fast
    return ['bsub'] + \
        (['-J', jobname] if jobname else []) + \
        ['-q', queue,
        '-W', time,
        '-oo', outfilepath,
        '-R', '"rusage[mem=' + str(int(memory_GB * 1024)) + \
                # '] select[model!=XeonE5345 && model!=XeonE5430 && model!=XeonE52680]"'] + \
                '] select[model!=XeonE5345 && model!=XeonE5430]"'] + \
            (['-w', 'done({})'.format(depends_on)] if depends_on is not None else []) + \
        [' '.join(command)]

# submits a command to LSF
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

# retrieves the elments of some array that are meant to be processed in a given batch
# batch_num is 1-indexed, as with LSF
def elements_in_batch(elements, batch_num, num_per_batch):
    return elements[(batch_num - 1) * num_per_batch:
            min(batch_num * num_per_batch, len(elements))]

# determines how many batches will be required to process a given number of elements
def num_batches(num_elements, num_per_batch):
    return int(math.ceil(num_elements / num_per_batch))

# creates main, submit, and merge argparsers, with each set to be triggered by the
# corresponding command-line keyword. this is for instances in which we want all three
# functions in the same file, with the ability to specify via command-line which one we
# will run. See choose_subparser_and_run
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

# see add_main_and_submit
def choose_parser_and_run(parser):
    args, _ = parser.parse_known_args()
    pretty.print_namespace(args); print()

    args._func(args)



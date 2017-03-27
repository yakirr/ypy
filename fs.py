from __future__ import print_function, division
import os, resource

# Create directory if necessary. If the directory exists do nothing
def makedir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)

def makedir_for_file(path_to_file):
    makedir(os.path.dirname(path_to_file))

def add_prefix(path_to_file, prefix):
    directory, fname = os.path.split(path_to_file)
    if not directory:
        directory = '.'
    if fname:
        return '/'.join([directory, prefix + fname])
    else:
        print('WARNING: cannot add prefix to directory', path_to_file)
        return path_to_file

def make_hidden(path_to_file):
    return add_prefix(path_to_file, '.')

def replace_ext(path_to_file, new_extension):
    root, ext = os.path.splitext(path_to_file)
    return root + '.' + new_extension

def mem():
    print('memory usage:', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000, 'Mb')


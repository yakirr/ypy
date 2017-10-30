from __future__ import print_function, division
import os, resource

# create a directory if it doesn't exist already
def makedir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)

# create a directory to house a given file
def makedir_for_file(path_to_file):
    makedir(os.path.dirname(path_to_file))

# add a prefix to a given filename
def add_prefix(path_to_file, prefix):
    directory, fname = os.path.split(path_to_file)
    if not directory:
        directory = '.'
    if fname:
        return '/'.join([directory, prefix + fname])
    else:
        print('WARNING: cannot add prefix to directory', path_to_file)
        return path_to_file

# return the filename corresponding to a hidden version of a given file
def make_hidden(path_to_file):
    return add_prefix(path_to_file, '.')

# replace a file's extension
def replace_ext(path_to_file, new_extension):
    root, ext = os.path.splitext(path_to_file)
    return root + '.' + new_extension

# return memory usage in MB
def mem():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000


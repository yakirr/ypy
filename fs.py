from __future__ import print_function, division
import os

# Create directory if necessary. If the directory exists do nothing
def makedir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)

def makedir_for_file(path_to_file):
    makedir(os.path.dirname(path_to_file))

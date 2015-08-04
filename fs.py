from __future__ import print_function, division
import os

# Create directory if necessary
def makedir(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

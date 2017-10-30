from __future__ import print_function, division
import collections
import itertools
import sys
from time import time

# wraps any iterable, and prints a progress report as it runs through
# that iterable
def show_progress(iterable, increment_percent=1, verbose=False, total=100):
    # if we can determine the size of the iterable, then use that to determine progress
    if isinstance(iterable, collections.Sized):
        total = len(iterable)
    stepsize = max(int(increment_percent / 100 * total), 1)
    t0 = time()
    for i, x in itertools.izip(xrange(total), iterable):
        if i % stepsize == 0:
            if not verbose:
                print('.', end='')
            else:
                print(
                    int((time() - t0) * 100) / 100,
                    ':',
                    int(i / total * 10000) / 100,
                    'percent complete (' + str(i) + ' of ' + str(total) + ')')
            sys.stdout.flush()
        yield x
    print('\n')

# returns chunks of a certain size
def grouper(chunk_size, iterable):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, chunk_size))
        if not chunk:
            return
        yield chunk

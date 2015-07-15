from __future__ import print_function, division
import collections
import itertools
import sys
from time import time

def show_progress(iterable, increment_percent=1, verbose=False, total=100):
	if isinstance(iterable, collections.Sized):
		total = len(iterable)
	stepsize = max(int(increment_percent / 100 * total), 1)
	t0 = time()
	for i, x in zip(xrange(total), iterable):
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
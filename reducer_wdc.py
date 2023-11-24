#!/usr/bin/env python3
"""reducer_wdc.py"""

from operator import itemgetter
import sys

current_origin = None
current_count = 0

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    origin, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_origin == origin:
        current_count += count
    else:
        if current_origin:
            # write result to STDOUT
            print('%s\t%s' % (current_origin, current_count))
        current_count = count
        current_origin = origin

# do not forget to output the last word if needed!
if current_origin == origin:
    print('%s\t%s' % (current_origin, current_count))

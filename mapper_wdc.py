#!/usr/bin/env python3
"""mapper_wdc.py"""

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    if not line:
        continue

    values = line.split('\t')
    origin = values[0]
    target = values[1]
    print('%s\t%s' % (origin, 1))

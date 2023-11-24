#!/usr/bin/env python3
"""mapper_join.py"""

import sys

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # split the input line into key and value
    data = line.split('\t')
    if len(data) == 2:
        key, value = data
        if key.isdigit():
            link_id = key
            sum_result = value
            link = '-'
        else:
            link = key
            link_id = value
            sum_result = '-'
        print('%s\t%s\t%s' % (link_id, link, sum_result))
    elif len(data) == 1:
        print('%s\t%s\t%s' % (data[0], '-', '-'))


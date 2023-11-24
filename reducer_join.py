#!/usr/bin/env python3
"""reducer_join.py"""

import sys

current_key = None
current_link = None
current_sum_result = 0

# Create a list to store records
records = []
outputs = []
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # split the input line into key, link, and sum_result
    splitted = line.split('\t', 2)
    if len(splitted) == 3:
        records.append(splitted)

# Sort the records based on the key
records.sort(key=lambda x: x[0])

# Process the sorted records
for record in records:
    key, link, sum_result = record

    # convert sum_result to int
    if sum_result.isdigit():
        sum_result = int(sum_result)
    else:
        sum_result = 0

    # process the input
    if current_key == key:
        current_sum_result += sum_result
        if link != '-':
            current_link = link
    else:
        if current_key:
            # write result to STDOUT
            outputs.append([current_link, current_sum_result])
            #print('%s\t%s' % (current_link, current_sum_result))
        current_key = key
        current_link = link
        current_sum_result = sum_result


if current_key == key:
    outputs.append([current_link, current_sum_result])

outputs.sort(key=lambda x: x[1], reverse=True)
for output in outputs:
    print('%s\t%s' % (output[0], output[1]))


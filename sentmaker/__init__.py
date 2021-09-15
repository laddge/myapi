#!/usr/bin/env python3
from random import randint
import os


def main():
    output = ''
    count_a = 0
    count_n = 0

    dictpath = os.path.join(os.path.dirname(__file__), 'dict.csv')
    with open(dictpath) as f:
        lines = f.read().split('\n')

    while True:
        line = lines[randint(0, len(lines) - 1)]
        if line.split(',')[1] == 'n':
            output = line.split(',')[0]
            count_n += 1
            break

    while True:
        line = lines[randint(0, len(lines) - 1)]
        if line.split(',')[1] == 'a':
            output = line.split(',')[0] + 'い' + output
            count_a += 1
            break

    while True:
        line = lines[randint(0, len(lines) - 1)]
        if line.split(',')[1] == 'a':
            if count_a < 3:
                output = line.split(',')[0] + 'くて' + output
                count_a += 1
        if line.split(',')[1] == 'n':
            if count_n < 3:
                output += 'と' + line.split(',')[0]
                count_n += 1
        if line.split(',')[1] == 'v':
            if count_a >= 3 and count_n >= 3:
                output += 'を' + line.split(',')[0]
                break
    return output

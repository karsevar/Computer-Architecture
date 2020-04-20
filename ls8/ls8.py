#!/usr/bin/env python3

"""Main."""
import re
import sys
from cpu import *

# write a load function that will take a file path 
# as an argument file path is sys.argv[1]

def load(file_path):
    with open(file_path, 'r', newline=None) as f:
        commands = f.readlines()
        new_commands = []
        for instruction in commands:
            # print(instruction.rstrip('\n'))
            if instruction.startswith('0') or instruction.startswith('1'):
                instruction_mod = instruction.split()
                new_commands.append(instruction_mod[0])

    return new_commands

new_commands = load(sys.argv[1])

print(new_commands)

cpu = CPU()

cpu.load()
# cpu.run()
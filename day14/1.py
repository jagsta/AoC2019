import sys
import re

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

for line in f.readlines():
    #Parse the reactions into a tree/graph
    match=re.match(r'((\d+ \w+),*)+ => (\d+ \w+)',line.strip())


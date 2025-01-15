import sys
import intcode

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(c)

program=intcode.intcode(code)

print(program)

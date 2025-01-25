import sys
import intcode
import copy

file="input.txt"
cmdfile="cmd.txt"

def print_grid(grid):
    for line in grid:
        s=""
        for c in line:
            s+=c
        print(s)

f=open(file)

code=intcode.GrowingList()

for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)
backup=copy.deepcopy(program)

print(program)

f=open(cmdfile)
cmds=[]
for i,line in enumerate(f.readlines()):
    cmds.append([])
    for cmd in line.rstrip("\n"):
        cmds[i].append(ord(cmd))
    cmds[i].append(10)

print(cmds)
s=""
cmd=[]
while True:
    r,v=program.execute(cmd)
    if r==0:
        print(s.rstrip("\n"))
        s=""
        print(r,v)
        if len(cmds)>0:
            cmd=cmds.pop(0)
    if r==1:
        try:
            s+=chr(v)
        except:
            s+=str(v)
    if r==99:
        print(s.rstrip("\n"))
        print(r,v)
        break

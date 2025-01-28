import sys
import intcode
import copy
from collections import deque

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

network=[]
queuein=[]
queueout=[]
last=[]

for t in range(50):
    network.append(copy.deepcopy(program))
    queuein.append(deque())
    queueout.append(deque())
    r,v=network[t].execute([t])
    last.append(r)
    print(t,r,v)

while True:
    for t in range(50):
        if len(queuein[t])>0:
            r,v=network[t].execute([queuein[t].popleft()])
        else:
            r,v=network[t].execute([-1])
        if r==1:
            queueout[t].append(v)
            print(t,r,v)
        elif r==99:
            break
        if len(queueout[t])>2:
            target=queueout[t].popleft()
            if target==255:
                raise ValueError(f'message to {target}: X:{queueout[t].popleft()} Y:{queueout[t].popleft()}')
            else:
                queuein[target].append(queueout[t].popleft())
                queuein[target].append(queueout[t].popleft())






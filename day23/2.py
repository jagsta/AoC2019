import sys
import intcode
import copy
from collections import deque
print(sys.maxsize)

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
natmsgs=0

for t in range(50):
    network.append(copy.deepcopy(program))
    queuein.append(deque())
    queueout.append(deque())
    r,v=network[t].execute([t])
    last.append(r)
    print(t,r,v)

nat=deque()
idleCount=0
allIdle=False
while True:
    if allIdle:
        idleCount+=1
    else:
        idleCount=0
    queueEmpty=True
    allIdle=True
    for t in range(50):
        if last[t]==0:
            if len(queuein[t])>0:
                queueEmpty=False
                r,v=network[t].execute([queuein[t].popleft()])
            else:
                r,v=network[t].execute([-1])
            #print(t,r,v)
        elif last[t]==1:
            r,v=network[t].execute([-1])
        if r==1:
            allIdle=False
            queueout[t].append(int(v))
            last[t]=1
            print(t,r,v)
        elif r==0:
            last[t]=0
        elif r==99:
            break
        if len(queueout[t])>2:
            target=queueout[t].popleft()
            if target==255:
                nat.clear()
                x=queueout[t].popleft()
                y=queueout[t].popleft()
                nat.append(x)
                nat.append(y)
                print(f'queueing x:{x},y:{y} for {target}, it now has queue {nat}')
            else:
                x=queueout[t].popleft()
                y=queueout[t].popleft()
                queuein[target].append(x)
                queuein[target].append(y)
                print(f'queueing x:{x},y:{y} for {target}, it now has queue {queuein[target]}')
    if allIdle and idleCount>0 and queueEmpty and len(nat)==2:
        print(queuein)
        print(queueout)
        x=nat.popleft()
        y=nat.popleft()
        print(f'sending x:{x} y:{y} to 0')
        queuein[0].append(x)
        queuein[0].append(y)
        if y==natmsgs:
            print(f'repeated NAT msg is Y:{y}')
            break
        else:
            print(f'adding y:{y} as last NAT msg')
            natmsgs=y







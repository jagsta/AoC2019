import sys
import intcode
import copy

dirs=[{"d":"n","x":0,"y":-1,"i":"^"},{"d":"e","x":1,"y":0,"i":">"},{"d":"s","x":0,"y":1,"i":"v"},{"d":"w","x":-1,"y":0,"i":"<"}]
file="input.txt"

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

grid=[]
gdict={}
count=0
for y in range(100):
    grid.append([])
    for x in range(100):
        program.pointer=0
        program.offset=0
        program.paramode={1:0,2:0,3:0}
        program.data=copy.copy(backup.data)
        r,v=program.execute([x,y])
        if r==99:
            break
        elif r==1:
            if v==1:
                grid[y].append("#")
                count+=1
            elif v==0:
                grid[y].append(".")
            gdict[(x,y)]=v


print_grid(grid)
print(count)

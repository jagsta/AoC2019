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

#100175 120277    100274 120178
#1121 1345 1220 1246 1 0
#1122 1346 1221 1247 1 0
#1123 1348 1222 1249 1 1
r,v = program.execute([1122,1347])
print(r,v)
program=copy.deepcopy(backup)
r,v = program.execute([1221,1248])
print(r,v)
program=copy.deepcopy(backup)

extremes=[(0,0),(99,-99)]
x=899
y=1068

while True:
    blcout=False
    while True:
        r,v = program.execute([x,y])
        program=copy.deepcopy(backup)
        if v==1:
            if blcout==True:
                break
            else:
                y+=1
        elif v==0:
            blcout=True
            x+=1
    r,v = program.execute([x+99,y-99])
    program=copy.deepcopy(backup)
    print(x,y,x+99,y-99,r,v)
    if v==1:
        print("YO, IT FITS BOY")
        break
    #print(x,y,"  ",x+99,y-99)
print("Final:",x,y)
print("Answer",(x-1)*10000+(y-1-99))





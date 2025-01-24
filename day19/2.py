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
xoffset=0
beamwidth=105
beamheight=0
xinc=7
yinc=9
minx=0
miny=0
maxy=2000
maxx=700
yreached=0
for y in range(miny,miny+maxy):
    grid.append([])
    inbeam=False
    thisbeam=0
    xd=0
    if xoffset>=maxx-2:
        yreached=y
        print(xoffset,y,beamwidth)
        break
    for x in range(minx,minx+maxx):
        if x<xoffset:
            grid[y].append(".")
            continue
        if x>xoffset or x>xoffset+beamwidth:
            program.pointer=0
            program.offset=0
            program.paramode={1:0,2:0,3:0}
            program.data=copy.copy(backup.data)
            r,v=program.execute([x,y])
            if r==1:
                if v==1:
                    if x>xoffset and not inbeam:
                        inbeam=True
                        xoffset=x-1
                        xd=1
                    if xd<beamwidth:
                        grid[y].extend(["#"]*beamwidth)
                        count=count+beamwidth
                        xd+=beamwidth
                        thisbeam=beamwidth
                    elif x>=xoffset+xd:
                        grid[y].append("#")
                        thisbeam+=1
                        count+=1
                elif v==0:
                    if inbeam:
                        grid[y].extend(["."]*(maxx-x))
                        if beamwidth<thisbeam:
                            beamwidth=thisbeam
                        break
                    grid[y].append(".")

                gdict[(x,y)]=v
            elif r==99:
                break

#print_grid(grid)
print(grid[yreached-1])

print(count)
print(beamwidth)

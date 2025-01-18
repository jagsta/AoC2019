import sys
import intcode
sys.setrecursionlimit(100000)

file="input.txt"

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)

print(program)

grid={} # key = x.y, value=0 (wall), 1(space), 2(target)
dirs=[{"d":"n","x":0,"y":-1,"n":2},{"d":"s","x":0,"y":1,"n":1},{"d":"w","x":-1,"y":0,"n":0},{"d":"e","x":1,"y":0,"n":3}]

def try_move(direction,x,y):
    #check each direction, add each to grid{}, if space and not in grid recurse, if target return 1, if no spaces or none not visited, return 0
    for i in range(0,4):
        d=(i+dirs[direction]["n"])%4
        r,result=program.execute([d+1]) #intcode takes directions 1-4
        print("trying",dirs[d]["d"],"from",x,y,"found",result)
        grid[str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"])]=result
        if result==0:
            #wall
            continue
        elif result==1:
            #space, we have moved
            x=x+dirs[d]["x"]
            y=y+dirs[d]["y"]
            r=try_move(d,x,y)
            return r
        elif result==2:
            # we've found the target
            print("FOUND IT at ",x+dirs[d]["x"],y+dirs[d]["y"])
            return 1
    return 0

found=False
grid["0.0"]=1
result=try_move(0,0,0)
print(result)

print(grid)

minx=0
maxx=0
miny=0
maxy=0
for p in grid:
    coords=p.split(".")
    x=int(coords[0])
    y=int(coords[1])
    if x>maxx:
        maxx=x
    if x<minx:
        minx=x
    if y>maxy:
        maxy=y
    if y<miny:
        miny=y

print(maxx-minx,maxy-miny)
gridmap=[["?" for i in range(maxx-minx+1)] for j in range(maxy-miny+1)]
for p,i in grid.items():
    if i==0:
        c="#"
    elif i==1:
        c="."
    elif i==2:
        c="O"
    coords=p.split(".")
    if coords[0]=="0" and coords[1]=="0":
        c="*"
    x=int(coords[0])-minx
    y=int(coords[1])-miny
    gridmap[y][x]=c

for line in gridmap:
    s=""
    for c in line:
        s+=c
    print(s)



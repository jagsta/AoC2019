import sys
import intcode
import networkx as nx
import copy
sys.setrecursionlimit(10000)


file="input.txt"

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)
backup=copy.deepcopy(program)

print(program)


G=nx.Graph()

grid={} # key = x.y, value=0 (wall), 1(space), 2(target)
#Changed dirs to be clockwise rotation, mapped to actual input commands as dirs[i]["n"]
dirs=[{"d":"n","x":0,"y":-1,"n":1},{"d":"e","x":1,"y":0,"n":4},{"d":"s","x":0,"y":1,"n":2},{"d":"w","x":-1,"y":0,"n":3}]

def try_move(direction,x,y,step):
    #check each direction, add each to grid{}, if space and not in grid recurse, if target return 1, if no spaces or none not visited, return 0
    if step==1:
        rmin=0
        rmax=4
    elif step==-1:
        rmin=3
        rmax=-1
    for i in range(rmin, rmax, step):
        if step==1:
            d=(i+direction-1)%4 #Try left of current direction
        elif step==-1:
            d=(i+direction-2)%4 #Try left of current direction
        r,result=program.execute([dirs[d]["n"]]) #intcode takes directions 1-4
        print("trying",dirs[d]["d"],"from",x,y,"found",result)
        grid[str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"])]=result
        if result==0:
            #wall
            continue
        elif result==1:
            #space, we have moved
            G.add_edge(str(x)+"."+str(y),str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"]))
            x=x+dirs[d]["x"]
            y=y+dirs[d]["y"]
            r=try_move(d,x,y,step)
            return r
        elif result==2:
            # we've found the target
            print("FOUND IT at ",x+dirs[d]["x"],y+dirs[d]["y"])
            G.add_edge(str(x)+"."+str(y),str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"]))
            return str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"])
    return r

grid["0.0"]=1
#try ccw, reset robot then try cw to maximise coverage
target=try_move(0,0,0,1)
program=copy.deepcopy(backup)
target=try_move(0,0,0,-1)

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

missed=0
squares=0
for line in gridmap:
    s=""
    for c in line:
        if c=="?":
            missed+=1
        elif c==".":
            squares+=1
        s+=c
    print(s)

print("target is",target,"squares missed in grid:",missed,"total squares to oxygenate is:",squares)
distance=nx.dijkstra_path_length(G, "0.0", target)
print(distance)

#Now we have a full map of visitable squares, we can fill with O by ticks until there are no spaces remaining.
ticks=0
distances=nx.single_source_shortest_path_length(G, "16.16")
for w in sorted(distances, key=distances.get):
    print(w, distances[w])

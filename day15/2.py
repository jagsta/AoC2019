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
dirs=[{"d":"n","x":0,"y":-1,"n":2},{"d":"s","x":0,"y":1,"n":1},{"d":"w","x":-1,"y":0,"n":0},{"d":"e","x":1,"y":0,"n":3}]
miss={}
miss["c"]=4

def try_move(direction,x,y):
    #check each direction, add each to grid{}, if space and not in grid recurse, if target return 1, if no spaces or none not visited, return 0
    for i in range(0,4):
        d=(i+dirs[direction]["n"])%4
        r,result=program.execute([d+1]) #intcode takes directions 1-4
        miss["c"]-=1
        print("trying",dirs[d]["d"],"from",x,y,"found",result,"unresolved is",miss["c"])
        grid[str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"])]=result
        if result==0:
            #wall
            continue
        elif result==1:
            #space, we have moved
            G.add_edge(str(x)+"."+str(y),str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"]))
            x=x+dirs[d]["x"]
            y=y+dirs[d]["y"]
            for t in dirs:
                if str(x+t["x"])+"."+str(y+t["y"]) not in grid:
                    miss["c"]+=1
            r=try_move(d,x,y)
            return r
        elif result==2:
            # we've found the target
            print("FOUND IT at ",x+dirs[d]["x"],y+dirs[d]["y"])
            G.add_edge(str(x)+"."+str(y),str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"]))
            return str(x+dirs[d]["x"])+"."+str(y+dirs[d]["y"])
    return r

grid["0.0"]=1
target=try_move(0,0,0)

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
for line in gridmap:
    s=""
    for c in line:
        if c=="?":
            missed+=1
        s+=c
    print(s)

print("target is",target,"algo thinks missed",miss["c"],"actual missed in grid",missed)
distance=nx.dijkstra_path_length(G, "0.0", target)
print(distance)

#Everything below here is suspect :)

for y,line in enumerate(gridmap):
    for x,c in enumerate(line):
        if c==".":
            for d in range(4):
                if y>0 and y<maxy-miny and x>0 and x<maxx-minx and gridmap[y+dirs[d]["y"]][x+dirs[d]["x"]]=="?":
                    try:
                        path=list(nx.shortest_path(G, str(0)+"."+str(0), str(x+minx)+"."+str(y+miny)))
                    except:
                        print(x+minx,y+miny,"not in G")
                        continue
                    print(str(x+minx)+"."+str(y+miny),"has path length",len(path))
                    working=copy.deepcopy(backup)
                    for i,a in enumerate(path[:-1]):
                        b = path[i+1]
                        #print(a,b)
                        ac=a.split(".")
                        bc=b.split(".")
                        ax=int(ac[0])
                        ay=int(ac[1])
                        bx=int(bc[0])
                        by=int(bc[1])
                        dx=bx-ax
                        dy=by-ay
                        #print(dx,dy)
                        if dx>0:
                            nd=4
                        elif dx<0:
                            nd=3
                        elif dy>0:
                            nd=2
                        else:
                            nd=1
                        #print(nd)
                        r,rv=working.execute([nd])
                        if rv==0:
                            break
                        #print(rv)
                    r,rv=working.execute([d])
                    if rv==0:
                        gridmap[y+dirs[d]["y"]][x+dirs[d]["x"]]="#"
                    else:
                        gridmap[y+dirs[d]["y"]][x+dirs[d]["x"]]="."
                        r=try_move(d,x+dirs[d]["x"],y+dirs[d]["y"])

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
        if c=="?":
            missed+=1
        s+=c
    print(s)

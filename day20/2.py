import sys
from collections import deque
from collections import defaultdict
import networkx as nx
import itertools


file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

portals=defaultdict()
grid=[]
gdict={}
for y,line in enumerate(f.readlines()):
    grid.append([])
    for x,c in enumerate(line.rstrip('\n')):
        if c=="." or c.isupper() or c=="#":
            gdict[(x,y)]="."
            grid[y].append(c)
        else:
            grid[y].append(" ")

xmax=len(grid[2])-1
ymax=len(grid)-1
print(xmax,ymax)
for line in grid:
    s=""
    for c in line:
        s+=c
    print(s)

for y in range(ymax):
    for x in range(xmax):
        c=grid[y][x]
        c2=grid[y][x+1]
        if c.isupper() and c2.isupper():
            if x==0:
                pname=str(c+c2+"+")
                print(pname,x,y)
                portals[pname]=(x+2,y)
            if x>xmax//2 and x<xmax-1:
                pname=str(c+c2+"-")
                print(pname,x,y)
                portals[pname]=(x+2,y)
            if x==xmax-1:
                pname=str(c+c2)+"+"
                print(pname,x,y)
                portals[pname]=(x-1,y)
            if x<xmax//2 and x>1:
                pname=str(c+c2+"-")
                print(pname,x,y)
                portals[pname]=(x-1,y)

for x in range(xmax):
    for y in range(ymax):
        c=grid[y][x]
        c2=grid[y+1][x]
        if c.isupper() and c2.isupper():
            if y==0:
                pname=str(c+c2+"+")
                print(pname,x,y)
                portals[pname]=(x,y+2)
            if y>ymax//2 and y<ymax-1:
                pname=str(c+c2+"=")
                print(pname,x,y)
                portals[pname]=(x,y+2)
            if y==ymax-1:
                pname=str(c+c2+"+")
                print(pname,x,y)
                portals[pname]=(x,y-1)
            if y<ymax//2 and y>1:
                pname=str(c+c2+"-")
                print(pname,x,y)
                portals[pname]=(x,y-1)

print(grid)
for i in portals:
    print(i,portals[i])

G = nx.Graph()
P = nx.Graph()
for y in range(2,ymax):
    for x in range(2,xmax):
        if grid[y][x]==".":
            for a,b in [(1,0),(0,1),(-1,0),(0,-1)]:
                if grid[y+b][x+a]==".":
                    G.add_edge((x,y),(x+a,y+b))

for i in itertools.combinations(portals,2):
     try:
         p = nx.shortest_path(G, portals[i[0]], portals[i[1]])
         print(i[0],i[1],len(p))
         P.add_edge(i[0],i[1],steps=len(p)-1)
     except:
         pass

for node in P.nodes():
    print (node, list(P.neighbors(node)))

for portal in portals:
    if portal=="AA":
        origin=portals[portal].pop()
    elif portal=="ZZ":
        target=portals[portal].pop()
    else:
        G.add_edge(portals[portal].pop(),portals[portal].pop())

path=nx.shortest_path(G, origin, target)
print(path)
print(len(path)-1)


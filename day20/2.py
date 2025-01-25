import sys
from collections import deque
from collections import defaultdict
import networkx as nx
import itertools
from math import inf


file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

portals=defaultdict()
grid=[]
for y,line in enumerate(f.readlines()):
    grid.append([])
    for x,c in enumerate(line.rstrip('\n')):
        if c=="." or c.isupper() or c=="#":
            grid[y].append(c)
        else:
            grid[y].append(" ")

xmax=len(grid[2])-1
ymax=len(grid)-1
#print(xmax,ymax)
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
#                print(pname,x,y)
                portals[pname]=(x+2,y)
            if x>xmax//2 and x<xmax-1:
                pname=str(c+c2+"-")
#                print(pname,x,y)
                portals[pname]=(x+2,y)
            if x==xmax-1:
                pname=str(c+c2)+"+"
#                print(pname,x,y)
                portals[pname]=(x-1,y)
            if x<xmax//2 and x>1:
                pname=str(c+c2+"-")
#                print(pname,x,y)
                portals[pname]=(x-1,y)

for x in range(xmax):
    for y in range(ymax):
        c=grid[y][x]
        c2=grid[y+1][x]
        if c.isupper() and c2.isupper():
            if y==0:
                pname=str(c+c2+"+")
#                print(pname,x,y)
                portals[pname]=(x,y+2)
            if y>ymax//2 and y<ymax-1:
                pname=str(c+c2+"-")
#                print(pname,x,y)
                portals[pname]=(x,y+2)
            if y==ymax-1:
                pname=str(c+c2+"+")
#                print(pname,x,y)
                portals[pname]=(x,y-1)
            if y<ymax//2 and y>1:
                pname=str(c+c2+"-")
#                print(pname,x,y)
                portals[pname]=(x,y-1)

#print(grid)
#for i in portals:
#    print(i,portals[i])

P = nx.Graph()
G = nx.Graph()
for y in range(2,ymax):
    for x in range(2,xmax):
        if grid[y][x]==".":
            for a,b in [(1,0),(0,1),(-1,0),(0,-1)]:
                if grid[y+b][x+a]==".":
                    G.add_edge((x,y),(x+a,y+b))

for i in itertools.combinations(portals,2):
     try:
         p = nx.shortest_path(G, portals[i[0]], portals[i[1]])
#         print(i[0],i[1],len(p))
         P.add_edge(i[0],i[1],steps=len(p)-1)
     except:
         pass

pneighbors=defaultdict(lambda:{})
for node in P.nodes():
    for n in P.neighbors(node):
#        if n=="ZZ+" or n=="AA+":
#            layer=0
#        elif n[2:]=="-":
#            layer=1
#        elif n[2:]=="+":
#            layer=-1
        pneighbors[node][n]={"layer":0,"cost":P.edges[node,n]['steps']}
        #print (node,n,layer)
#        print (node,n)


for portal in portals:
    if portal=="AA+":
        origin=portals[portal]
    elif portal=="ZZ+":
        target=portals[portal]
    elif portal[2:]=="+":
        pair=str(portal[:2]+"-")
        pneighbors[portal][pair]={"layer":-1,"cost":1}
        #pneighbors[portal][pair]={"layer":0,"cost":1}
    elif portal[2:]=="-":
        pair=str(portal[:2]+"+")
        pneighbors[portal][pair]={"layer":1,"cost":1}
        #pneighbors[portal][pair]={"layer":0,"cost":1}
    else:
        raise ValueError(f'no pair found for portal {portal}')


#for node in pneighbors:
#    print(node,pneighbors[node])

def pathfind(origin,target,startlayer=0,targetlayer=0,maxsteps=10000,maxlayers=len(pneighbors)):
    heap=deque()
    distance=0
    final_dist=inf
    final_path=""
    best_ds=defaultdict(lambda:inf)
    best_ds[(origin,startlayer)]=distance
    heap.append((origin,startlayer,distance,origin))
    while len(heap)>0:
        o,l,d,p = heap.popleft()
#        print(o,l,d)
        # Firstly, can we bail? have we been at this node at this layer with fewer steps?
        if best_ds[(o,l)]<d:
#            print(f'pruning {o},{l},{d} - best ds {best_ds[(o,l)]}')
            continue
        if d>maxsteps or abs(l)>maxlayers:
            continue
            #raise ValueError('Too many steps taken: {d} exceeds {maxsteps}')
        if o==target and l==0:
#            print(f'reached the end {o} at layer {l} with distance {d}')
            if final_dist>best_ds[(o,l)]:
                final_dist=best_ds[(o,l)]
                final_path=p
        #may be more to check here?
        for k,v in pneighbors[o].items():
            thisp=p
            thisl=l
            thisd=d
            thisd+=v['cost']
            thisl+=v['layer']
            thisp+=","+str(thisl)+","+k
            if best_ds[(k,thisl)]<thisd or (k=="ZZ+" and thisl!=0) or thisl<0:
                continue
            else:
#                print(f'{o} {l} {d} neighbor: {k} {v} new layer {thisl}, new dist {thisd}')
                best_ds[(k,thisl)]=thisd
                heap.append((k,thisl,thisd,thisp))
    return final_dist,final_path

result,path=pathfind("AA+","ZZ+")
print(f'distance:{result}\npath:{path}')

import sys
import itertools
import networkx as nx
from collections import deque

file="input.txt"
dirs=[[0,-1],[1,0],[0,1],[-1,0]]

def k2bm(k,bm):
    # stores the presence of a key labelled a-z in a bitmask
    return bm + (1<<(ord(k)-ord("a")))

def bm2k(k,bm):
    # checks for the presence of a key labelled a-z in a bitmask
    return True if bm^(1<<ord(k)-ord("a"))==0 else False

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)
G=nx.Graph()
P=nx.Graph()

# integer representation of all keys bitmap, generated as the map is parsed
# when a search equals fullmap, we have all keys
fullmap=0

heap=deque()

origin=""
keys={}
c2keys={}
keys2c={}
c2locks={}
locks2c={}
kandls={}
okeys={}
gdict={}
klmap={}
y=0
x=0
for line in f.readlines():
    for c in line.strip():
        gdict[(x,y)]=c
        if c!="#":
            if c.isupper():
                print("Lock",c,"at",x,y)
                c2locks[(x,y)]=c
                locks2c[c]=(x,y)
                kandls[(x,y)]=c
                G.add_node((x,y),c=c)
            elif c.islower():
                print("key",c,"at",x,y)
                fullmap=k2bm(c,fullmap)
                keys[(x,y)]=c
                okeys[(x,y)]=c
                keys2c[(x,y)]=c
                c2keys[c]=(x,y)
                kandls[(x,y)]=c
                G.add_node((x,y),c=c)
            elif c=="@":
                print("origin at",x,y)
                origin=(x,y)
                kandls[(x,y)]=c
            for d in dirs:
                # Only add edges if it's not a lock
                #if c.isupper():
                #    break
                print("trying dir",d)
                newx=x+d[0]
                newy=y+d[1]
                #if str(newx)+"."+str(newy) in gdict and gdict[str(newx)+"."+str(newy)]!="#" and gdict[str(newx)+"."+str(newy)].isupper() is not True:
                if (newx,newy) in gdict and gdict[(newx,newy)]!="#":
                    #only add edges if it's not a lock
                    print(x,y,"is adjacent to a space")
                    G.add_edge((x,y),(newx,newy))

        x+=1
    x=0
    y+=1

print(f'fullmap value is {fullmap}')
print(c2locks)
print(locks2c)

print(origin)
okeys[origin]="@"
print(G.nodes)
print(G.edges)



#We now have a graph of paths which are not blocked by locks

#This doesnt' work, try using restricted_view with list of nodes supplied to suppress based on isLocked dict copies?

def permute(orig,length,k):
    global tried
    global pruned
    global shortest
    global best
    if tried%10000==0:
        print(f'tried {tried} paths and pruned {pruned}, current best path is {best} {shortest}')
    if best_ds[(orig,k)] < length:
#        print("Already too far, killing this path")
        pruned+=1
        continue
    for node in (P.neighbors(orig)):
#            print(orig,node)
        thisk=k
        if node.islower():
            thisk=k2bm(node,k)
        thisl=length+P.edges[orig][node]["steps"]
        if best_ds[(node,k)]<thisl:
            continue
        else:
            #FIX ME here
            thisl+=permute(node,k,l,thisl,thisph)
#        except Exception as error:
#            print("An exception occurred:", error)
#            continue
    return 0

#view=nx.subgraph_view(G,filter_node=filter_locks)
#print(f'view: {view.nodes}')
#for node in get_next(view,origin,keys)
#    pl = nx.shortest_path_length(view,origin,node)
#    P.add_edge(origin,node,steps=pl)

for i in itertools.combinations(kandls,2):
    p = nx.shortest_path(G, i[0], i[1])
    last=p[0]
    count=0
    for nstep in p[1:]:
        count+=1
        if nstep in kandls:
            P.add_edge(kandls[last],kandls[nstep],steps=count)
            count=0
            last=nstep



print(f'P Graph edges:\n{P.edges(data=True)}')
print(P.edges('@'))

tried=0
pruned=0
best=""
best_ds={}
shortest=10000000
print("possible paths:")
permute(origin,keysleft,locksleft,0,"")
print(shortest)
print(f'tried {tried}')
print(f'pruned {pruned}')

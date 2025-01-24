#Thoughts on how to approach this
# I need to iterate over the 4 robots to recheck whether they have a move possible
# I need to maintain a unique key bitmask which I pass to subsequent moves (whether of my robot or another of the 4)

# Peudo code:
# Add all 4 robots initial positions to the stack
# pop a state off the stack ( robot 1 initially)
# Repeat while there's state to process:
#
# Do we have all the keys?
#   If so, is the score lower than previous best?
#       If so, update best to this score
#           Bail this state
# Do we already have a shorter distance for this position/keymap combo?
#   if so, bail?
# Any valid moves? If yes, add each to the back of the stack with state (moves + keymask)
#   If a move available, check if any valid moves for the other 3 robots with that state, and add to the back of the stack
# Maybe try first with a single measure of moves(sum across any robot), this may work, as keymaps will vary
import sys
import itertools
import networkx as nx
from collections import deque
from collections import defaultdict
from math import inf

file="input.txt"
dirs=[[0,-1],[1,0],[0,1],[-1,0]]

def k2bm(k,bm):
    # stores the presence of a key labelled a-z in a bitmask
    #print(f'k2bm received {k} and {bin(bm)}, returning {bin(bm + (1<<(ord(k)-ord("a"))))}')
    return bm + (1<<(ord(k)-(ord("a")-1)))

def bm2k(k,bm):
    # checks for the presence of a key labelled a-z in a bitmask
    #print(f'bm2k received {k} and {bin(bm)}, returning {(True if bm&(1<<(ord(k)-(ord("a")-1)))>0 else False)}')
    return (True if bm&(1<<(ord(k)-(ord("a")-1)))>0 else False)

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)
G=nx.Graph()
P=nx.Graph()

# integer representation of all keys bitmap, generated as the map is parsed
# when a search equals fullmap, we have all keys
fullmap=0

heap=deque()
backheap=deque()

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
ocount=0
for line in f.readlines():
    for c in line.strip():
        gdict[(x,y)]=c
        if c!="#":
            if c.isupper():
                #print("Lock",c,"at",x,y)
                c2locks[(x,y)]=c
                locks2c[c]=(x,y)
                kandls[(x,y)]=c
                G.add_node((x,y),c=c)
            elif c.islower():
                #print("key",c,"at",x,y)
                fullmap=k2bm(c,fullmap)
                keys[(x,y)]=c
                okeys[(x,y)]=c
                keys2c[(x,y)]=c
                c2keys[c]=(x,y)
                kandls[(x,y)]=c
                G.add_node((x,y),c=c)
            elif c=="@":
                ocount+=1
                c+=str(ocount)
                print(f'origin {c} at {x,y}')
                origin=(x,y)
                kandls[(x,y)]=c
            for d in dirs:
                # Only add edges if it's not a lock
                #if c.isupper():
                #    break
                #print("trying dir",d)
                newx=x+d[0]
                newy=y+d[1]
                #if str(newx)+"."+str(newy) in gdict and gdict[str(newx)+"."+str(newy)]!="#" and gdict[str(newx)+"."+str(newy)].isupper() is not True:
                if (newx,newy) in gdict and gdict[(newx,newy)]!="#":
                    #only add edges if it's not a lock
                    #print(x,y,"is adjacent to a space")
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

def permute(oid1,oid2,oid3,oid4,length,key):
    global tried
    global pruned
    best_ds[(oid1,oid2,oid3,oid4,key)]=0
    heap.append((oid1,oid2,oid3,oid4,length,key))
    final_dist=inf
    if tried%10000==0:
        print(f'tried {tried} paths and pruned {pruned}, current best path is {best} {shortest}')
    while len(heap)>0:
        # take the oldest tuple off the stack
        o1,o2,o3,o4,l,k = heap.popleft()
        #Is this already worse than the best we've seen for this node with these keys?
        if best_ds[(o1,o2,o3,o4,k)]<l:
            #print("Already too far, killing this path")
            pruned+=1
            continue
        # Is this a tuple with all keys?
        if k==fullmap:
            #is it the best distance we've seen
            if best_ds[(o1,o2,o3,o4,k)]<final_dist:
                final_dist=best_ds[(o1,o2,o3,o4,k)]
                continue
        # for each robot
        for o in [o1,o2,o3,o4]:
            # for next hops from this node(o)
            for node in pneighbors[o]:
                thisk=k
                #if best_ds[(node,k)]<=l:
                #    pruned+=1
                #    continue
                # If lock and we don't have the key, abandon
                if node.isupper() and not bm2k(node.lower(),thisk):
                    continue
                # If key and we don't have it yet, add the key to mask
                if node.islower() and node[0]!='@' and not bm2k(node,thisk):
                    #print(bin(thisk))
                    thisk=k2bm(node,thisk)
                thisl=l+plengths[(o,node)]
                if o==o1:
                    t=(node,o2,o3,o4,thisk)
                    h=(node,o2,o3,o4,thisl,thisk)
                elif o==o2:
                    t=(o1,node,o3,o4,thisk)
                    h=(o1,node,o3,o4,thisl,thisk)
                elif o==o3:
                    t=(o1,o2,node,o4,thisk)
                    h=(o1,o2,node,o4,thisl,thisk)
                elif o==o4:
                    t=(o1,o2,o3,node,thisk)
                    h=(o1,o2,o3,node,thisl,thisk)
                if best_ds[t]<=thisl:
                    continue
                else:
                    #print(h,bin(thisk))
                    best_ds[t]=thisl
                    heap.append(h)


    return final_dist


#view=nx.subgraph_view(G,filter_node=filter_locks)
#print(f'view: {view.nodes}')
#for node in get_next(view,origin,keys)
#    pl = nx.shortest_path_length(view,origin,node)
#    P.add_edge(origin,node,steps=pl)

for i in itertools.combinations(kandls,2):
    try:
        p = nx.shortest_path(G, i[0], i[1])
        last=p[0]
        count=0
        for nstep in p[1:]:
            count+=1
            if nstep in kandls:
                P.add_edge(kandls[last],kandls[nstep],steps=count)
                count=0
                last=nstep
    except:
        pass



plengths={}
print(f'P Graph edges:\n{P.edges(data=True)}')
for a,b in P.edges:
    try:
        plengths[(a,b)]=P.edges[(a,b)]['steps']
        plengths[(b,a)]=P.edges[(a,b)]['steps']
    except:
        pass

print(plengths)

pneighbors={}
for a in P.nodes:
    pneighbors[a]=set(P.neighbors(a))

print(pneighbors)

tried=0
pruned=0
shortest=0
best=""
best_ds=defaultdict(lambda: inf)
shortest=permute("@1","@2","@3","@4",0,0)
print(shortest)
print(f'tried {tried}')
print(f'pruned {pruned}')

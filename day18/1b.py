import sys
import itertools
import networkx as nx

file="input.txt"
dirs=[[0,-1],[1,0],[0,1],[-1,0]]

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)
G=nx.Graph()
P=nx.Graph()

origin=""
keys={}
locks={}
okeys={}
gdict={}
klmap={}
y=0
x=0
for line in f.readlines():
    for c in line.strip():
        gdict[str(x)+"."+str(y)]=c
        if c!="#":
            if c.isupper():
                print("Lock",c,"at",x,y)
                locks[str(x)+"."+str(y)]=c
                G.add_node(str(x)+"."+str(y),char=c,isUnlocked=False)
            elif c.islower():
                print("key",c,"at",x,y)
                keys[str(x)+"."+str(y)]=c
                okeys[str(x)+"."+str(y)]=c
                G.add_node(str(x)+"."+str(y),char=c,isKey=True)
            elif c=="@":
                print("origin at",x,y)
                origin=str(x)+"."+str(y)
            for d in dirs:
                # Only add edges if it's not a lock
                #if c.isupper():
                #    break
                print("trying dir",d)
                newx=x+d[0]
                newy=y+d[1]
                #if str(newx)+"."+str(newy) in gdict and gdict[str(newx)+"."+str(newy)]!="#" and gdict[str(newx)+"."+str(newy)].isupper() is not True:
                if str(newx)+"."+str(newy) in gdict and gdict[str(newx)+"."+str(newy)]!="#":
                    #only add edges if it's not a lock
                    print(x,y,"is adjacent to a space")
                    G.add_edge(str(x)+"."+str(y),str(newx)+"."+str(newy))

        x+=1
    x=0
    y+=1

for key,value in keys.items():
    klmap[key]=None
    for lock,lvalue in locks.items():
        if value==lvalue.lower():
            klmap[key]=lock
print(klmap)

print(origin)
okeys[origin]="@"
print(gdict)
#We now have a graph of paths which are not blocked by locks
print(G.nodes(data=True))
print(G.edges)
print(keys)
keysleft=dict(keys)
locksleft=dict(locks)

#This doesnt' work, try using restricted_view with list of nodes supplied to suppress based on isLocked dict copies?

def permute(orig,keysleft,locksleft,length,ph):
    view=nx.restricted_view(P,locksleft,[])
#    print(view.nodes)
    global tried
    global pruned
    global shortest
    global best
    if tried%10000==0:
        print(f'tried {tried} paths and pruned {pruned}, current best path is {best} {shortest}')
    if shortest < length:
#        print("Already too far, killing this path")
        pruned+=1
        return 0
    for node in get_next(view,orig,keysleft):
#            print(orig,node)
            thisl=length+pathlengths[orig][node]
            thisph=ph+keys[node]
            k=keysleft.copy()
            k.pop(node)
            if len(k)>0:
                l=locksleft.copy()
                l.pop(klmap[node],None)
                thisl+=permute(node,k,l,thisl,thisph)
            else:
#                    print(f'final distance was {thisl} for path {thisph}')
                tried+=1
                if thisl<shortest:
                    shortest=thisl
                    best=ph
                    ph=""
#        except Exception as error:
#            print("An exception occurred:", error)
#            continue
    return 0

#view=nx.subgraph_view(G,filter_node=filter_locks)
#print(f'view: {view.nodes}')
#for node in get_next(view,origin,keys)
#    pl = nx.shortest_path_length(view,origin,node)
#    P.add_edge(origin,node,steps=pl)

pathlengths={}
isblocked={}
for i in itertools.combinations(okeys,2):
    if i[0] not in pathlengths:
        pathlengths[i[0]]={}
    if i[1] not in pathlengths:
        pathlengths[i[1]]={}
    if i[1] not in isblocked:
        isblocked[i[1]]={}
    if i[0] not in isblocked:
        isblocked[i[0]]={}
    p = nx.shortest_path(G, i[0], i[1])
    pathlengths[i[0]][i[1]]=len(p)-1
    pathlengths[i[1]][i[0]]=len(p)-1
    last=i[0]
    count=0
    for step in p[1:]:
        count+=1
        if step in locks or step in keys or step==origin:
            P.add_edge(last,step,steps=count)
            last=step
            count=0
            if step in keys:
                if i[0] not in isblocked[i[1]]:
                    isblocked[i[1]][i[0]]=set()
                if i[1] not in isblocked[i[0]]:
                    isblocked[i[0]][i[1]]=set()
                isblocked[i[1]][i[0]].add(step)
                isblocked[i[0]][i[1]].add(step)



for s in pathlengths:
    for t in pathlengths[s]:
        print(s,t,pathlengths[s][t])

for s in isblocked:
    for t in isblocked[s]:
        print(s,t,isblocked[s][t])

print(P.edges(data=True))

def get_next(graph,orig,keysleft):
    next=set()
    for key in keysleft:
        blocked=False
        if key in isblocked[orig]:
            for p in isblocked[orig][key]:
                if p in keysleft:
                    blocked=True
                    break
        if not blocked:
            if nx.has_path(graph,orig,key):
                next.add(key)
    return next

def filter_locks(node):
    #print(G.nodes[node].get('isUnlocked'))
    #return G.nodes[node]["isUnlocked"]
    return G.nodes[node].get('isUnlocked',True)

tried=0
pruned=0
best=""
shortest=10000000
print("possible paths:")
view=nx.subgraph_view(P,filter_node=filter_locks)
print(f'view: {view.edges}')
print(get_next(view,origin,keysleft))

permute(origin,keysleft,locksleft,0,"")
print(shortest)
print(f'tried {tried}')
print(f'pruned {pruned}')

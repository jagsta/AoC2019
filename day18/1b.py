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

def permute(graph,orig,keysleft,length,ph):
    view=nx.subgraph_view(graph,filter_node=filter_locks)
    print(view.nodes)
    global tried
    global pruned
    tried+=1
    if tried%100000==0:
        print(f'tried {tried} paths and pruned {pruned}')
    global shortest
    if shortest < length:
#        print("Already too far, killing this path")
        return 0
    for node in get_next(view,orig,keysleft):
            g=graph.copy()
            print(orig,node)
            thisl=length+pathlengths[orig][node]
            thisph=ph+keys[node]
            k=dict(keysleft)
            k.pop(node)
            g.nodes[node]['isUnlocked']=True
            if len(k)>0:
                thisl+=permute(g,node,k,thisl,thisph)
            else:
#                    print(f'final distance was {thisl} for path {thisph}')
                ph=""
                if thisl<shortest:
                    shortest=thisl
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
for i in itertools.combinations(okeys,2):
    if i[0] not in pathlengths:
        pathlengths[i[0]]={}
    if i[1] not in pathlengths:
        pathlengths[i[1]]={}
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


for s in pathlengths:
    for t in pathlengths[s]:
        print(s,t,pathlengths[s][t])

print(P.edges(data=True))

def get_next(graph,orig,keysleft):
    next=set()
    for key in keysleft:
        if nx.has_path(graph,orig,key):
            next.add(key)
    return next

def filter_locks(node):
    #print(G.nodes[node].get('isUnlocked'))
    #return G.nodes[node]["isUnlocked"]
    return G.nodes[node].get('isUnlocked',True)

tried=0
pruned=0
shortest=10000000
print("possible paths:")
view=nx.subgraph_view(P,filter_node=filter_locks)
print(f'view: {view.edges}')
print(get_next(view,origin,keysleft))

permute(P,origin,keysleft,0,"")
print(shortest)
print(f'tried {tried}')
print(f'pruned {pruned}')

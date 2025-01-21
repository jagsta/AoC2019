import sys
import networkx as nx

file="input.txt"
dirs=[[0,-1],[1,0],[0,1],[-1,0]]

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)
G=nx.Graph()

origin=""
keys={}
locks={}
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
                G.add_node(str(x)+"."+str(y),char=c,isLock=True)
            elif c.islower():
                print("key",c,"at",x,y)
                keys[str(x)+"."+str(y)]=c
                G.add_node(str(x)+"."+str(y),char=c,isKey=True)
            elif c=="@":
                print("origin at",x,y)
                origin=str(x)+"."+str(y)
            for d in dirs:
                print("trying dir",d)
                newx=x+d[0]
                newy=y+d[1]
                if str(newx)+"."+str(newy) in gdict and gdict[str(newx)+"."+str(newy)]!="#":
                    print(x,y,"is adjacent to a space")
                    G.add_edge(str(x)+"."+str(y),str(newx)+"."+str(newy))

        x+=1
    x=0
    y+=1

print(origin)
print(gdict)
print(G.nodes(data=True))
print(G.edges)
print(keys)
keysleft=dict(keys)
locksleft=dict(locks)

def permute(orig,locksleft,keysleft,length,ph):
    global tried
    tried+=1
    if tried%100000==0:
        print(f'tried {tried} paths')
    global shortest
    if shortest < length:
#        print("Already too far, killing this path")
        return 0
    for key in keysleft:
            thisl=length
            thisph=ph
#        try:
#            print(f'trying from {orig} to {keys[key]} at {key}, length is {length} and path is {ph}')
            path=nx.shortest_path(G,source=orig,target=key)
#            print(f'path is {path}')
            blocked=False
            for p in path:
                if p in locksleft:
#                    print(f'{p} is a key in locksleft, so blocked')
                    blocked=True
                    break
            if not blocked:
                thisph+=keys[key]
                thisl+=len(path)-1
#                print(orig,key,keys[key],len(path),thisl)
                k=dict(keysleft)
                k.pop(key)
#                print(f'{len(k)} keys left: {k}')
                l=dict(locksleft)
                for coord,lock in l.items():
#                    print(f'trying {keys[key].upper()} and {lock}')
                    if keys[key].upper()==lock:
                        l.pop(coord)
                        break
                if len(k)>0:
                    thisl+=permute(key,l,k,thisl,thisph)
                else:
#                    print(f'final distance was {thisl} for path {thisph}')
                    ph=""
                    if thisl<shortest:
                        shortest=thisl
#        except Exception as error:
#            print("An exception occurred:", error)
#            continue
    return 0
tried=0
shortest=10000000
print("shortest paths:")
permute(origin,locksleft,keysleft,0,"")
print(shortest)

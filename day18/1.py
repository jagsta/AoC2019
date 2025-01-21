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
gdict={}
y=0
x=0
for line in f.readlines():
    for c in line.strip():
        gdict[str(x)+"."+str(y)]=c
        if c!="#":
            if c.isupper():
                print("Lock",c,"at",x,y)
                G.add_node(str(x)+"."+str(y),char=c,isLock=True)
            elif c.islower():
                print("key",c,"at",x,y)
                keys[str(x)+"."+str(y)]=c
                G.add_node(str(x)+"."+str(y),char=c,isKey=True)
            elif c=="@":
                print("origin at",x,y)
                origin=str(x)+"."+str(y)
            for d in dirs:
                if c.isupper():
                    break
                print("trying dir",d)
                nx=x+d[0]
                ny=y+d[1]
                if str(nx)+"."+str(ny) in gdict and gdict[str(nx)+"."+str(ny)]!="#" and gdict[str(nx)+"."+str(ny)].isupper() is False:
                    print(x,y,"is adjacent to a space")
                    G.add_edge(str(x)+"."+str(y),str(nx)+"."+str(ny))

        x+=1
    x=0
    y+=1

print(origin)
print(gdict)
print(G.nodes(data=True))
print(G.edges)
print(keys)

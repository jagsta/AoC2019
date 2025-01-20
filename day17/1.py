import sys
import intcode
import copy
import networkx as nx

dirs=[{"d":"n","x":0,"y":-1,"i":"^"},{"d":"e","x":1,"y":0,"i":">"},{"d":"s","x":0,"y":1,"i":"v"},{"d":"w","x":-1,"y":0,"i":"<"}]
file="input.txt"

def print_grid(grid):
    for line in grid:
        s=""
        for c in line:
            s+=c
        print(s)

f=open(file)

code=intcode.GrowingList()

for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)
backup=copy.deepcopy(program)

print(program)

G=nx.Graph()

grid=[]
gdict={}
grid.append([])
y=0
x=0
while True:
    r,v=program.execute([])
    if r==99:
        break
    elif r==1:
        if v==10:
            grid.append([])
            y+=1
            x=0
        else:
            grid[y].append(chr(v))
            gdict[str(x)+"."+str(y)]=chr(v)
            x+=1

print_grid(grid)

for p,v in gdict.items():
    if v!=".":
        c=p.split(".")
        x=int(c[0])
        y=int(c[1])
        for d in dirs:
            nx=x+d["x"]
            ny=y+d["y"]
            if str(nx)+"."+str(ny) in gdict and gdict[str(nx)+"."+str(ny)]!=".":
                G.add_edge(str(x)+"."+str(y),str(nx)+"."+str(ny))

alignment=0
for n in G.degree():
    if n[1]>2:
        c=n[0].split(".")
        x=int(c[0])
        y=int(c[1])
        alignment+=x*y
        grid[y][x]="O"
        print(n)


print_grid(grid)
print(alignment)

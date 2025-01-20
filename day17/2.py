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

origin=""
tovisit=set()
for p,v in gdict.items():
    if v!=".":
        tovisit.add(p)
        if v=="^":
            origin=p
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

print(origin)
print(tovisit)
print(len(tovisit))

def nextsq(current,direction):
    c=current.split(".")
    x=int(c[0])
    y=int(c[1])
    nx=x+dirs[direction]["x"]
    ny=y+dirs[direction]["y"]
    if str(nx)+"."+str(ny) in gdict and gdict[str(nx)+"."+str(ny)]!=".":
        return str(nx)+"."+str(ny)
    else:
        return False

#part 2 - first, we need to build a set of instruction to arrive at end of scaffold
# algorithm - proceed as far as possible, if we can go right, turn right, if not, turn left

moves=""
direction=0 #starts north
movesize=0
current=origin
while True:
    n=nextsq(current,direction)
    if n:
        print(f'can move, next square is {n}')
        movesize+=1
        current=n
        tovisit.discard(current)
    else:
        if movesize>0:
            moves+=str(movesize)
        n=nextsq(current,(direction+1)%4)
        if n:
            moves+="R"
            movesize=0
            direction=(direction+1)%4
        else:
            n=nextsq(current,(direction-1)%4)
            if n:
                moves+="L"
                movesize=0
                direction=(direction-1)%4
            else:
                print("dead end")
                #if len(tovisit)==0:
                print(tovisit)
                break

print(moves)
#Manual inspection here gives the following:
#R4R10R8R4R10R6R4R4R10R8R4R10R6R4R4L12R6L12R10R6R4R4L12R6L12R4R10R8R4R10R6R4R4L12R6L12
A="R,4,R,10,R,8,R,4"
B="R,4,L,12,R,6,L,12"
C="R,10,R,6,R,4"
M="A,C,A,C,B,C,B,A,C,B"
F="n"
AA=[]
AB=[]
AC=[]
AM=[]
AF=[]
for i in A:
    AA.append(ord(i))
for i in B:
    AB.append(ord(i))
for i in C:
    AC.append(ord(i))
for i in M:
    AM.append(ord(i))
for i in F:
    AF.append(ord(i))

cmds=[AF,AC,AB,AA,AM]
for c in cmds:
    print(len(c))
    c.append(10)

print(AA)
print(AB)
print(AC)
print(AM)
print(AF)

cmd=[]
#print(program)
s=""
while True:
    r,v=program.execute(cmd)
    #print(r,v)
    if r==1:
        if v==10:
            print(s)
            s=""
        elif v<256:
            s+=chr(v)
        else:
            s+=str(v)
    elif r==0:
        cmd=cmds.pop()
        print("sending",cmd)
    elif r==99:
        print(s)
        print(r,v)
        break
    else:
        print("unknown response code",r,v)



import sys

file="input.txt"

f=open(file)

grid={}
y=0
x=0
for line in f.readlines():
    for c in line.strip():
        grid[(x,y)]=c
        x+=1
    y+=1
    x=0

print(grid)


def adj(coord):
    count=0
    for a in [(1,0),(0,-1),(-1,0),(0,1)]:
        if (coord[0]+a[0],coord[1]+a[1]) in grid and grid[(coord[0]+a[0],coord[1]+a[1])]=="#":
            count+=1
    return count

def next(current,count):
    if current=="#" and count!=1:
        return "."
    elif current=="." and (count==1 or count==2):
        return "#"
    else:
        return current

def calcstate(grid):
    score=0
    for coord,current in grid.items():
        if current=="#":
            score+=2**((coord[1])*5+coord[0])
    return score

states=set()
minutes=0

while True:
    new={}
    for coord,current in grid.items():
        count=adj(coord)
        new[coord]=next(current,count)
    state=calcstate(new)
    if state in states:
        print (f'repeated state observed, with score {state}:\n{new}')
        break
    else:
        states.add(state)
    grid=new.copy()

import sys

file="input.txt"

f=open(file)

gridlayers={}
y=0
x=0
gridlayers[0]=gridlayer(0)
for line in f.readlines():
    for c in line.strip():
        gridlayers[0][(x,y)]=c
        x+=1
    y+=1
    x=0

class gridlayer:
    def __init__(self,layer):
        self.layer=layer
        self.grid=[["." for y in range(5)] for x in range(5)]

    def getadj(self,coord):
        x=coord[0]
        y=coord[1]
        adj=0
        if x==0 or x==4 or y==0 or y==4:
            #outside edges, so adjacencies in layer -1
            layer=self.layer-1
            if layer not in gridlayers:
                gridlayers[layer]=gridlayer(layer)
            for c in ((1,0),(0,1),(-1,0),(0,-1)):
                if x+c[0]>4:
                    if gridlayers[layer][(2,3)]=="#":
                        adj+=1
                elif x+c[0]<0:
                    if gridlayers[layer][(2,1)]=="#":
                        adj+=1
                elif y+c[1]>4:
                    if gridlayers[layer][(3,2)]=="#":
                        adj+=1
                elif y+c[1]<0:
                    if gridlayers[layer][(1,2)]=="#":
                        adj+=1
                elif gridlayers[(y+c[0],x+c[1])]=="#":
                        adj+=1

        if 0<x<4 and 0<y<4:
            #adjacent to centre square, so adjacencies in layer +1
            layer=self.layer+1
            if layer not in gridlayers:
                gridlayers[layer]=gridlayer(layer)
            for c in ((1,0),(0,1),(-1,0),(0,-1)):
                if x+c[0]==2:
                    if y+c[1]==1:
                        ny=0
                    elif y+c[1]==3:
                        ny=4
                    for nx in range(5):
                        if gridlayers[layer][(ny,nx)]=="#":
                            adj+=1
                elif y+c[1]==2:
                    if x+c[0]==1:
                        nx=0
                    elif x+c[0]==3:
                        nx=4
                    for ny in range(5):
                        if gridlayers[layer][(ny,nx)]=="#":
                            adj+=1
                elif gridlayer[(y+c[0],x+c[1])]=="#":
                    adj+=1
        return adj

    def next(self,current,count):
        if current=="#" and count!=1:
            return "."
        elif current=="." and (count==1 or count==2):
            return "#"
        else:
            return current

    def calcstate(self):
        new={}
        for layer in gridlayers:
            new[layer]=gridlayer(layer)
            for coord,current in gridlayers[layer].items():
                count=getadj(current)
                new[layer][coord]=next(layer[coord],count)
        return new


print(grid)

def adj(coord):
    count=0
    for a in [(1,0),(0,-1),(-1,0),(0,1)]:
        if (coord[0]+a[0],coord[1]+a[1]) in grid and grid[(coord[0]+a[0],coord[1]+a[1])]=="#":
            count+=1
    return count

states=set()
minutes=0

while True:
    gridlayers=gridlayers[0].calcstate()
    minutes+=1
    if minutes=200:
        total=0
        for layer in gridlayers.values():
            for current in layer.values():
                if current=="#":
                    total+=1
        print(f'total bugs at minute {minute}: {total}')
        break




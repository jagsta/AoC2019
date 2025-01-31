import sys
import copy

file="input.txt"
targetmins=200

if len(sys.argv)>1:
    file=sys.argv[1]

if len(sys.argv)>2:
    targetmins=int(sys.argv[2])

f=open(file)


class gridlayer:
    def __init__(self,layer):
        self.layer=layer
        self.grid={}
        for y in range(5):
            for x in range(5):
                if x==2 and y==2:
                    self.grid[(x,y)]="?"
                else:
                    self.grid[(x,y)]="."

    def getadj(self,coord):
        x=coord[0]
        y=coord[1]
        adj=0
        if x==0 or x==4 or y==0 or y==4:
            #outside edges, so adjacencies in layer -1
            layer=self.layer-1
            for c in ((1,0),(0,1),(-1,0),(0,-1)):
                if layer in gridlayers:
                    if x+c[0]>4:
                        if gridlayers[layer].grid[(3,2)]=="#":
                            adj+=1
                    elif x+c[0]<0:
                        if gridlayers[layer].grid[(1,2)]=="#":
                            adj+=1
                    elif y+c[1]>4:
                        if gridlayers[layer].grid[(2,3)]=="#":
                            adj+=1
                    elif y+c[1]<0:
                        if gridlayers[layer].grid[(2,1)]=="#":
                            adj+=1
                if (x+c[0],y+c[1]) in self.grid and self.grid[(x+c[0],y+c[1])]=="#":
                    adj+=1

        if 0<x<4 and 0<y<4:
            #adjacent to centre square, so adjacencies in layer +1
            layer=self.layer+1
            if layer in gridlayers:
                if x==2:
                    if y==1:
                        ny=0
                        for nx in range(5):
                            if gridlayers[layer].grid[(nx,ny)]=="#":
                                adj+=1
                    elif y==3:
                        ny=4
                        for nx in range(5):
                            if gridlayers[layer].grid[(nx,ny)]=="#":
                                adj+=1
                elif y==2:
                    if x==1:
                        nx=0
                        for ny in range(5):
                            if gridlayers[layer].grid[(nx,ny)]=="#":
                                adj+=1
                    elif x==3:
                        nx=4
                        for ny in range(5):
                            if gridlayers[layer].grid[(nx,ny)]=="#":
                                adj+=1
            for c in ((1,0),(0,1),(-1,0),(0,-1)):
                if (x+c[0],y+c[1]) in self.grid and self.grid[(x+c[0],y+c[1])]=="#":
                    adj+=1
        return adj

    def next(self,current,count):
        if current=="#" and count!=1:
            return "."
        elif current=="." and (count==1 or count==2):
            return "#"
        else:
            return current

    def calcstate(self,current,count):
        return self.next(current,count)

    def checkrecursion(self):
        layers=set()
        for coord,current in self.grid.items():
            x=coord[0]
            y=coord[1]
            if current=="#":
                if x==0 or x==4 or y==0 or y==4:
                    print(f'bug in outer cell in layer:{self.layer}, adding {self.layer-1}')
                    layers.add(self.layer-1)
                if ((x==1 or x==3) and y==2) or ((y==1 or y==3) and x==2):
                    print(f'bug in inner cell in layer:{self.layer}, adding {self.layer+1}')
                    layers.add(self.layer+1)
        return layers

gridlayers={}
y=0
x=0
gridlayers[0]=gridlayer(0)
for line in f.readlines():
    for c in line.strip():
        gridlayers[0].grid[(x,y)]=c
        x+=1
    y+=1
    x=0
for y in range(5):
    s=""
    for x in range(5):
        s+=gridlayers[0].grid[(x,y)]
    print(s)


minutes=0
layers=set()
oldlayers=set()
layers.add(0)

#I've broken this, need to rethink how we manage additional layers sensibly

while True:
    newgrid={}
    low=min(layers)
    high=max(layers)
    #print(f'checking recursion at layers {low} and {high}')
    layers.update(gridlayers[low].checkrecursion())
    layers.update(gridlayers[high].checkrecursion())
    for layer in layers:
    #    print(f'checking layer:{layer}')
        if layer not in gridlayers:
            gridlayers[layer]=gridlayer(layer)
        newgrid[layer]=gridlayer(layer)
        for coord in gridlayers[layer].grid:
            if not (coord[0]==2 and coord[1]==2):
                count=gridlayers[layer].getadj(coord)
                newgrid[layer].grid[coord]=gridlayers[layer].calcstate(gridlayers[layer].grid[coord],count)
                print(f'layer {layer} checking adj count for {coord}:{count}, current {gridlayers[layer].grid[coord]},new {newgrid[layer].grid[coord]}')
    gridlayers=copy.deepcopy(newgrid)
    minutes+=1
    print(f'minute:{minutes}, layers:{len(layers)}')
    for layer in gridlayers:
        print(layer)
        for y in range(5):
            s=""
            for x in range(5):
                s+=gridlayers[layer].grid[(x,y)]
            print(s)
    if minutes==targetmins:
        total=0
        for layer in gridlayers.values():
            print(f'counting bugs in layer {layer}')
            for current in layer.grid.values():
                if current=="#":
                    total+=1
        print(f'total bugs at minute {minutes}: {total}')
        for l,layer in enumerate(gridlayers.values()):
            print(l)
            for y in range(5):
                s=""
                for x in range(5):
                    s+=layer.grid[(x,y)]
                print(s)
        break

import sys
import intcode

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)

print(program)

class robot:
    def __init__(self):
        self.dirs={"^":{"x":"0","y":"-1","r":">","l":"<"},">":{"x":"1","y":"0","r":"v","l":"^"},"v":{"x":"0","y":"1","r":"<","l":">"},"<":{"x":"-1","y":"0","l":"v","r":"^"}}
        self.path={"0.0":0}
        self.dir="^"
        self.cur="0.0"


    def move(self,colour,turn):
        # Set the current square colour as directed
        self.path[self.cur]=colour
        # process the direction change
        if turn==0:
            #left
            self.dir=self.dirs[self.dir]["l"]
        elif turn==1:
            self.dir=self.dirs[self.dir]["r"]
        else:
            raise ValueError("invalid direction",turn)
        # move the robot based on current direction
        coords=self.cur.split(".")
        x=int(coords[0])+int(self.dirs[self.dir]["x"])
        y=int(coords[1])+int(self.dirs[self.dir]["y"])
        self.cur=str(x)+"."+str(y)
        # Do we have an existing colour for this square? If not, it's black as newly visited
        if self.cur not in self.path:
            self.path[self.cur]=0
        return int(self.path[self.cur])

r=robot()
colour=1
s=0
while True:
    s,colour=program.execute([colour])
    if s==99:
        break
    #print(s,colour)
    s,turn=program.execute()
    if s==99:
        break
    #print(s,turn)
    print("robot move",colour,turn,r.cur)
    c=r.move(colour,turn)
    colour=int(c)

#        s,turn=program.execute()
#        if s=="99":
#            break
#        if s=="1":
#            colour=r.move(int(colour),int(turn))
#
#print(r.path)
#print(len(r.path))
maxh=0
minh=0
maxw=0
minw=0
for p,c in r.path.items():
    coord=p.split(".")
    if int(coord[0])>maxw:
        maxw=int(coord[0])
    if int(coord[1])>maxh:
        maxh=int(coord[1])
    if int(coord[0])<minw:
        minw=int(coord[0])
    if int(coord[1])<minh:
        minh=int(coord[1])
print(maxh,minh,maxw,minw)
pixels=[[" " for i in range(maxw-minw+1)] for j in range(maxh-minh+1)]
print(len(pixels))
print(len(pixels[0]))
for p,c in r.path.items():
    coord=p.split(".")
    if c==1:
        pixels[int(coord[1])][int(coord[0])]="#"
    else:
        pixels[int(coord[1])][int(coord[0])]=" "
for line in pixels:
    s=""
    for c in line:
        s+=c
    print(s)

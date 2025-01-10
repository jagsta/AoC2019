import sys

class node:
    def __init__(self,data):
        self.data = data
        self.prei = None

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f = open(file)

wire1={}
wire2={}
n=0
d=[]
for line in f.readlines():
    n+=1
    wires=line.strip().split(",")
    x=0
    y=0
    z=0
    for wire in wires:
        if wire[0]=="R":
            d=[1,0]
        elif wire[0]=="L":
            d=[-1,0]
        elif wire[0]=="U":
            d=[0,1]
        elif wire[0]=="D":
            d=[0,-1]
        last=str(x)+"."+str(y)

        for i in range(int(wire[1:])):
            z+=1
            if n==1:
                #print("adding",str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))," to wire1")
                if str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1))) not in wire1:
                    wire1[str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))]=z
                tx=x+(d[0]*(i+1))
                ty=y+(d[1]*(i+1))
                last=str(tx)+"."+str(ty)
            elif n==2:
                #print("adding",str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))," to wire2")
                if str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1))) not in wire2:
                    wire2[str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))]=z
                tx=x+(d[0]*(i+1))
                ty=y+(d[1]*(i+1))
                last=str(tx)+"."+str(ty)
        x=tx
        y=ty

mandist=10000000
manticks=10000000
for i in wire1:
    if i in wire2:
        print(i)
        coords=i.split(".")
        dist=abs(int(coords[0]))+abs(int(coords[1]))
        ticks=wire1[i]+wire2[i]
        if dist<mandist:
            mandist=dist
        if ticks<manticks:
            manticks=ticks

print(mandist)
print(manticks)


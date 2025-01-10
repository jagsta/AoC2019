import sys

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

#FIX ME - wire paths overlap themselves, so we overwrite the previous and cause loops in the length calculation, need a pre for each direction we hit a grid pos, and then to use that to look up the correct pre in the length loop
        for i in range(int(wire[1:])):
            if n==1:
                #print("adding",str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))," to wire1")
                wire1[str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))][wire[0]]=last
                tx=x+(d[0]*(i+1))
                ty=y+(d[1]*(i+1))
                last=str(tx)+"."+str(ty)
            elif n==2:
                #print("adding",str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))," to wire2")
                wire2[str(x+(d[0]*(i+1)))+"."+str(y+(d[1]*(i+1)))][wire[0]]=last
                tx=x+(d[0]*(i+1))
                ty=y+(d[1]*(i+1))
                last=str(tx)+"."+str(ty)
        x=tx
        y=ty

mandist=10000000
manticks=1000000
w1ticks=0
w2ticks=0
for i in wire1:
    if i in wire2:
        print(i)
        coords=i.split(".")
        p=i
        while True:
            d=wire1[p][0]
            print(p,w1ticks)
            w1ticks+=1
            p=wire1[p]
            if p=="0.0":
                break
        p=i
        while True:
            print(p,w1ticks)
            w2ticks+=1
            p=wire2[p]
            if p=="0.0":
                break
        dist=abs(int(coords[0]))+abs(int(coords[1]))
        ticks=w1ticks+w2ticks
        if dist<mandist:
            mandist=dist
        if ticks<manticks:
            manticks=ticks

print(mandist)
print(ticks)


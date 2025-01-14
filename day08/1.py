file="input.txt"

f=open(file)

maxw=25
maxh=6
layers=[]

h=1
w=1
l=0
for line in f.readlines():
    for c in line.strip():
        if w==1 and h==1:
            layers.append([])
        layers[l].append(int(c))
        if w==maxw:
            w=0
            if h==maxh:
                h=0
                l+=1
            h+=1
        w+=1

m0=maxw*maxh
total=0
for layer in layers:
    c0=0
    c1=0
    c2=0
    for c in layer:
        if c==0:
            c0+=1
        if c==1:
            c1+=1
        if c==2:
            c2+=1
    if c0<=m0:
        m0=c0
        total=c1*c2
        print("found",c0,"zeros, which is less than",m0,"new total is",c1,"x",c2,"=",total)

print(total)



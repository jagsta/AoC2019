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

print(layers)

pixels=[[None for i in range(maxw)] for j in range(maxh)]
#for line in pixels:
#    print(len(line))
for layer in layers:
    for j,c in enumerate(layer):
        i=j // 25
        j=j % 25
        print(i,j)
        if c==0 and pixels[i][j] is None:
            pixels[i][j]=" "
        if c==1 and pixels[i][j] is None:
            pixels[i][j]="#"

for line in pixels:
    print(line)


import sys

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f = open(file)

orbits={}
for line in f.readlines():
    orbit=line.strip().split(")")
    if orbit[0] in orbits:
        orbits[orbit[0]].append(orbit[1])
    else:
        orbits[orbit[0]]=[orbit[1]]

print(orbits)

root=""
for k in orbits.keys():
    if not any(k in v for v in orbits.values()):
        #this is the root object
        print("root is",k)
        root=k
        break

values={}

def score(key,value):
    if key in orbits.keys():
        for i in orbits[key]:
            values[i]=value
            score(i,value+1)

score(root,1)

print(values)
total=0
for v in values.values():
    total+=v

print(total)



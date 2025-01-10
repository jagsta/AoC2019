import sys

f = open("input.txt")

total=0
ftotal=0
for line in f.readlines():
    i=int(line.strip())
    i=(i//3)-2
    total+=i
    j=int(line.strip())
    while j>0:
        j=(j//3)-2
        if j>0:
            ftotal+=j

print(total)
print(ftotal)

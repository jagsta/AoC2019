f=open("input.txt")

def isDouble(num):
    s=str(num)
    last=""
    for c in s:
        if c==last:
            return True
        last=c
    return False

def rises(num):
    s=str(num)
    last=0
    for i in s:
        if int(i)<last:
            return False
        last=int(i)
    return True

passwords=[]
for line in f.readlines():
    space=line.split("-")
    for i in range(int(space[0]),int(space[1])+1):
        if isDouble(i) and rises(i):
            passwords.append(i)
            print(i,"matches")

print(len(passwords))

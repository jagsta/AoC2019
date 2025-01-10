f=open("input.txt")

def isDouble(num):
    s=str(num)
    last=""
    runs={}
    for c in s:
        if c==last:
            if c in runs:
                runs[c]+=1
            else:
                runs[c]=2
        last=c
    for run in runs:
        if runs[run]==2:
            return True
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

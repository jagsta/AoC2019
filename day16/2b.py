#New insight: the last half of the computed number can be calculated by summing the previous phase digits mod 10
# for pos x of length n, next phase is sum of x..n mod10 for all positions > len/2
# If the offset is greater than len/2, we can compute just those numbers using the above method to obtain the result


import time
import sys
import functools
from math import lcm

file="input.txt"
arraysize=10000

if len(sys.argv)>1:
    file=sys.argv[1]

if len(sys.argv)>2:
    arraysize=int(sys.argv[2])

data=[]
f=open(file)
for line in f.readlines():
    for c in line.strip():
        data.append(int(c))

n=""
for i in range(7):
    n+=str(data[i])

offset=int(n)


print(data)
print(len(data))
data=data*arraysize
#print(data)
print(len(data))
print(offset)
if offset>len(data)//2:
    print("optimised path available")
print(f'code at phase 0 is {data[offset+1:offset+9]}')
string=data[offset:]
substring=string[::-1]
print(len(substring))
print(substring[-8:])
#print(substring)
phases=0
maxphase=100

while True:
    result=[]
    last=0
    for i in range(len(substring)):
        this=(last+substring[i])
        result.append(this%10)
        last=this
    substring=result.copy()
    print(substring[0:100])
    phases+=1
    print(f'phase {phases} complete')
    if phases==maxphase:
        answer=substring[::-1]
        a=""
        for i in range(8):
            a+=str(answer[i])
        print(a)
        break

import sys
import functools
from math import lcm

file="input.txt"
arraysize=1

if len(sys.argv)>1:
    file=sys.argv[1]

if len(sys.argv)>2:
    arraysize=int(sys.argv[2])

data=[]
f=open(file)
for line in f.readlines():
    for c in line.strip():
        data.append(int(c))

uniquesize=len(data)
print(data)
print(len(data))
data=data*arraysize
#print(data)
print(len(data))
@functools.cache
def subsum(sublist):
    #print(sublist,type(sublist))
    sum=0
    for i in sublist:
        sum+=int(i)
    return sum

repeats={}

for i in range(1,len(data)+1):
    r=int(lcm(i*4,uniquesize)/uniquesize)
    if r<arraysize:
        repeats[i]=r

print(repeats)

offset=False
digits=8
chunksize=int(len(data)/16)
maxphases=100
phases=0
mask=[0,1,0,-1]
# Still way too slow - other ways to make efficient?
# take each sublist and pass to function, cache result. Each sublist will either be summed or inverse summed
# 2nd Optimisation insight:
# if the input pattern is repeated, then the mask for a given position will also repeat in some width divisible by 4x(i+1) (so 4 for pos 1, 8 for 2, 12 for pos 3 etc
# If we know when the pattern repeats, we can reuse those calculations x n to build the rest of the sum, and therefore the digit
# This should reduce the number of calcs significantly for lower positions, less drastically for higher
# see notes for workings on formula to calculate repeat length for a given i (wip)
# for character i:
# repeat happens after math.lcm((i+1)*masklength,uniquesize)/uniquesize
while True:
    result=[]
    #for each digit in the overall input
    for i in range(len(data)):
        sum=0
        neg=False
        # starting at index j (which increases in steps of i+1 as the mask grows)
        for j in range(i,len(data),2*(i+1)):
            #print(f'i:{i},j:{j}')
            #if i+1 is even, the mask is either 1 or -1, otherwise it's 0 and the sum will be 0
            substring="".join(str(x) for x in data[j:j+i+1])
            if neg:
                sum-=subsum(str(substring))
                neg=False
            else:
                sum+=subsum(str(substring))
                neg=True

                #take the next k digits from index
#                for k in range(i+1):
#                    if j+k<len(data):
#                        w=data[j+k]
#                        sum+=calc(i,j,w)
#                    else:
#                        break
#            print(f'i:{i},j:{j},w:{w},multiplier:{multiplier},maskindex:{maskindex}')

        result.append(int(str(sum)[-1]))
#        print(result)
    phases+=1
    print("phases complete:",phases)
    data=result.copy()
    if phases==maxphases:
        if offset:
            o=int(str(result[0:7]))
        else:
            o=0
        s=""
        for i in range(digits):
            s+=str(result[i+offset])
        print(s)
        break

import sys
import functools

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

data=[]
f=open(file)
for line in f.readlines():
    for c in line.strip():
        data.append(int(c))

uniquesize=len(data)
arraysize=10
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

multiplier=1
while True:
    if (uniquesize*multiplier)%4==0:
        break
    mutliplier+=1
print(f'multiplier is {multiplier} for input length {uniquesize}')
for i in range(1,len(data)):
    repeats[i]=int(uniquesize*i*(multiplier))

print(repeats)

offset=True
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
            for k in range(0,len(substring),chunksize):
                if neg:
                    sum-=subsum(str(k))
                    neg=False
                else:
                    sum+=subsum(str(k))
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

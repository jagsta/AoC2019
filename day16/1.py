import sys

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

data=[]
f=open(file)
for line in f.readlines():
    for c in line.strip():
        data.append(int(c))

arraysize=1000
print(data)
print(len(data))
data=data*arraysize
#print(data)
print(len(data))

digits=8
maxphases=100
phases=0
mask=[0,1,0,-1]
while True:
    result=[]
    for i in range(len(data)):
        sum=0
        for j,w in enumerate(data):
            m=((j+1)//(i+1))%4
            if m==3:
                sum-=w
            elif m==1:
                sum+=w
            else:
                continue
#            print(f'i:{i},j:{j},w:{w},multiplier:{multiplier},maskindex:{maskindex}')

        result.append(int(str(sum)[-1]))
    phases+=1
    print(phases)
    data=result.copy()
    if phases==maxphases:
        s=""
        for i in range(digits):
            s+=str(result[i])
        print(s)
        break

import sys

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

data=[]
f=open(file)
for line in f.readlines():
    for c in line.strip():
        data.append(int(c))

print(data)

digits=8
maxphases=100
phases=0
mask=[0,1,0,-1]
while True:
    result=[]
    multiplier=0
    for i in range(len(data)):
        sum=0
        multiplier+=1
        for j,w in enumerate(data):
            maskindex=((j+1)//multiplier)%4
#            print(f'i:{i},j:{j},w:{w},multiplier:{multiplier},maskindex:{maskindex}')
            sum+=w*mask[maskindex]
        result.append(int(str(sum)[-1]))
    phases+=1
    data=result.copy()
    if phases==maxphases:
        s=""
        for i in range(digits):
            s+=str(result[i])
        print(s)
        break

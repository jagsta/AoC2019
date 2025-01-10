f=open("input.txt")

class intcode:
    def __init__(self,data):
        self.data=data
        self.pointer=0

    def read(self,pointer=self.pointer):
        #placeholder

def execute(intcode,noun,verb):
    intcode[1]=noun
    intcode[2]=verb
    for i in range(0,len(intcode),4):
        opcode=intcode[i+0]
        a=intcode[intcode[i+1]]
        b=intcode[intcode[i+2]]
        if opcode==1:
            intcode[intcode[i+3]]=a+b
        elif opcode==2:
            intcode[intcode[i+3]]=a*b
        elif opcode==99:
            break
    return intcode

intcode=[]
for line in f.readlines():
    for c in line.strip().split(","):
        intcode.append(int(c))

answer=[]
for noun in range(100):
    for verb in range(100):
        program=intcode.copy()
        result=execute(program,noun,verb)
        if result[0]==19690720:
            answer=result.copy()
            break

print(answer[0],(100*answer[1])+answer[2])


import sys
from itertools import permutations
import copy

din=[1]
if len(sys.argv)>1:
    din=int(sys.argv[1])

f=open("input.txt")

class intcode:
    def __init__(self,data):
        self.data=data
        self.pointer=0

    def get_opcode(self):
        #placeholder
        word=str(self.data[self.pointer])
#        print(self.pointer,word)
        self.paramode1=0
        self.paramode2=0
        self.paramode3=0
        if len(word)<3:
            self.opcode=int(word)
        else:
            self.opcode=int(str(self.data[self.pointer])[-2:])
            if len(word)>=5:
                self.paramode3=int(word[-5])
            if len(word)>=4:
                self.paramode2=int(word[-4])
            if len(word)>=3:
                self.paramode1=int(word[-3])
        return self.opcode

    def execute(self,din=None):
        halt=False
        output=""
        while True:
            if halt:
                break
            opc=self.get_opcode()
#            print(self.pointer,opc,output)
            if opc==1:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2==1:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                self.data[self.data[self.pointer+3]]=a+b
                self.pointer+=4
            elif opc==2:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2==1:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                self.data[self.data[self.pointer+3]]=a*b
                self.pointer+=4
            elif opc==3:
                self.data[self.data[self.pointer+1]]=din.pop(0)
                self.pointer+=2
            elif opc==4:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                output+=str(a)
                self.pointer+=2
            elif opc==5:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2==1:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                if a!=0:
                    self.pointer=b
                else:
                    self.pointer+=3
            elif opc==6:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2==1:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                if a!=0:
                    self.pointer+=3
                else:
                    self.pointer=b
            elif opc==7:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2==1:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                if a<b:
                    self.data[self.data[self.pointer+3]]=1
                else:
                    self.data[self.data[self.pointer+3]]=0
                self.pointer+=4
            elif opc==8:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2==1:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                if a==b:
                    self.data[self.data[self.pointer+3]]=1
                else:
                    self.data[self.data[self.pointer+3]]=0
                self.pointer+=4
            elif opc==99:
                halt=True
                self.pointer+=1
            else:
                return "invalid opcode"
        return output

code=[]
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode(code)
print(program)


maxthrust=0
phases=list(permutations(range(0,5)))
for phase in phases:
    print("trying",phase)
    output=0
    for i in range(0,5):
        current=copy.deepcopy(program)
        din=[phase[i],output]
        output=int(current.execute(din))
    if output>maxthrust:
        print(output,"achieved for phase",phase,"previous best",maxthrust)
        maxthrust=output

print(maxthrust)

#result=program.execute(din)

#print(result)

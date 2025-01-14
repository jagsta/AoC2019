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
        while True:
            if halt:
                break
            opc=self.get_opcode()
            print(self.pointer,opc)
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
                if len(din)<1:
                    return 0,0
                self.data[self.data[self.pointer+1]]=din.pop(0)
                self.pointer+=2
            elif opc==4:
                if self.paramode1==1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                self.pointer+=2
                return 1,int(a)
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
                return 99,0
            else:
                raise ValueError("invalid opcode")

code=[]
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode(code)
print(program)


maxthrust=0
phases=list(permutations(range(5,10)))
for phase in phases:
    print("trying",phase)
    output=0
    ampa=copy.deepcopy(program)
    ampb=copy.deepcopy(program)
    ampc=copy.deepcopy(program)
    ampd=copy.deepcopy(program)
    ampe=copy.deepcopy(program)
    ina=[phase[0]]
    inb=[phase[1]]
    inc=[phase[2]]
    ind=[phase[3]]
    ine=[phase[4]]
#    print(ina,inb,inc,ind,ine)
    rca,ina=ampa.execute(ina)
    rcb,inb=ampb.execute(inb)
    rcc,inc=ampc.execute(inc)
    rcd,ind=ampd.execute(ind)
    rce,ine=ampe.execute(ine)
#    print(ina,inb,inc,ind,ine)
    ina=0
    while True:
        rca,inb=ampa.execute([ina])
        rcb,inc=ampb.execute([inb])
        rcc,ind=ampc.execute([inc])
        rcd,ine=ampd.execute([ind])
        rce,ina=ampe.execute([ine])
        if rce==1:
            output=ina
        if rce==99:
            break
        print(output)
    if output>maxthrust:
        print(output,"achieved for phase",phase,"previous best",maxthrust)
        maxthrust=output

print(maxthrust)

#result=program.execute(din)

#print(result)

f=open("input.txt")

class intcode:
    def __init__(self,data):
        self.data=data
        self.pointer=0

    def get_opcode(self):
        #placeholder
        word=str(self.data[self.pointer])
        self.paramode1=0
        self.paramode2=0
        self.paramode3=0
        if len(word)<2:
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
            print(self.pointer,opc,output)
            if opc==1:
                if self.paramode1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                self.data[self.data[self.pointer+3]]=a+b
                self.pointer+=4
            elif opc==2:
                if self.paramode1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                if self.paramode2:
                    b=self.data[self.pointer+2]
                else:
                    b=self.data[self.data[self.pointer+2]]
                self.data[self.data[self.pointer+3]]=a*b
                self.pointer+=4
            elif opc==3:
                self.data[self.pointer+1]=din
                self.pointer+=2
            elif opc==4:
                if self.paramode1:
                    a=self.data[self.pointer+1]
                else:
                    a=self.data[self.data[self.pointer+1]]
                output+=str(a)
                self.pointer+=2
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

result=program.execute(1)

print(result)

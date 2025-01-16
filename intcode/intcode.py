import sys

class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)

class intcode:
    def __init__(self,data):
        self.data=data
        self.pointer=0
        # param mode 0=position mode (value at location specified), 1=immediate mode (value), 2=relative mode (value at relative position specified)
        self.paramode={1:0,2:0,3:0}
        self.offset=0

    def __str__(self):
        s=""
        for c in self.data:
            s+=str(c)+","
        return f'{s[:-1]}\npointer:{self.pointer}\noffset:{self.offset}\nparammodes:{self.paramode}'

    def get_value(self,param):
        # param should be integer value from 1 to 3
        try:
            mode=self.paramode[param]
        except:
            raise ValueError("invalid parameter number")
        if mode==0:
            try:
                return self.data[self.data[self.pointer+param]]
            except:
                #print("index out of range, growing program")
                self.data[self.data[self.pointer+param]]=0
                return 0
        elif mode==1:
            try:
                return self.data[self.pointer+param]
            except:
                #print("index out of range, growing program")
                self.data[self.pointer+param]=0
                return 0
        elif mode==2:
            try:
                return self.data[self.offset+self.data[self.pointer+param]]
            except:
                #print("index out of range, growing program")
                self.data[self.offset+self.data[self.pointer+param]]=0
                return 0
        else:
            raise ValueError("parameter mode undefined")

    def set_value(self,param,value):
        # param should be integer value from 1 to 3
        try:
            mode=self.paramode[param]
        except:
            raise ValueError("invalid parameter number")
        if mode==0:
            #print("setting position",param,self.data[self.pointer+param],"to",value,type(value))
            self.data[int(self.data[self.pointer+param])]=value
        elif mode==1:
            raise ValueError("write attempted in immediate mode")
        elif mode==2:
            self.data[self.offset+self.data[self.pointer+param]]=value
        else:
            raise ValueError("parameter mode undefined")

    def get_opcode(self):
        #placeholder
        word=str(self.data[self.pointer])
#        print(self.pointer,word)
        # Reset param modes
        for param in self.paramode:
            self.paramode[param]=0
        if len(word)<3:
            self.opcode=int(word)
        else:
            self.opcode=int(str(self.data[self.pointer])[-2:])
            if len(word)>=5:
#                print("setting param 3 mode to",int(word[-5]))
                self.paramode[3]=int(word[-5])
            if len(word)>=4:
#                print("setting param 2 mode to",int(word[-4]))
                self.paramode[2]=int(word[-4])
            if len(word)>=3:
#                print("setting param 1 mode to",int(word[-3]))
                self.paramode[1]=int(word[-3])
        return self.opcode

    def execute(self,din=""):
        halt=False
        while True:
            if halt:
                break
            opc=self.get_opcode()
            #print(self.pointer,opc)
            if opc==1:
                a=self.get_value(1)
                b=self.get_value(2)
                self.set_value(3,a+b)
                self.pointer+=4
            elif opc==2:
                a=self.get_value(1)
                b=self.get_value(2)
                self.set_value(3,a*b)
                self.pointer+=4
            elif opc==3:
                if len(din)<1:
                    return 0,0
                self.set_value(1,din.pop(0))
                self.pointer+=2
            elif opc==4:
                a=self.get_value(1)
                self.pointer+=2
                return 1,int(a)
            elif opc==5:
                a=self.get_value(1)
                b=self.get_value(2)
                if a!=0:
                    self.pointer=b
                else:
                    self.pointer+=3
            elif opc==6:
                a=self.get_value(1)
                b=self.get_value(2)
                if a!=0:
                    self.pointer+=3
                else:
                    self.pointer=b
            elif opc==7:
                a=self.get_value(1)
                b=self.get_value(2)
                if a<b:
                    self.set_value(3,1)
                else:
                    self.set_value(3,0)
                self.pointer+=4
            elif opc==8:
                a=self.get_value(1)
                b=self.get_value(2)
                if a==b:
                    self.set_value(3,1)
                else:
                    self.set_value(3,0)
                self.pointer+=4
            elif opc==9:
                a=self.get_value(1)
                self.offset+=a
#                print("offset changed by",a,"to",self.offset)
                self.pointer+=2
            elif opc==99:
                halt=True
                self.pointer+=1
                return 99,0
            else:
                raise ValueError("invalid opcode at",self.pointer,": ",opc)

#code=GrowingList()
#for line in f.readlines():
#    for c in line.strip().split(","):
#        code.append(int(c))
#
#program=intcode(code)
#print(program)
#
#result=""
#while True:
#    rc,output=program.execute([din])
#    if rc==99:
#        break
#    if rc==1:
#        print(output)
#        result+=str(output)+","
#
#
#print(result)

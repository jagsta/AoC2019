import sys
import intcode

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(c)

program=intcode.intcode(code)

print(program)

class robot:
    def __init__(self):
        self.dirs={"^":{x:"0",y:"-1",r:">",l:"<"},">":{x:"1",y:"0",r:"v",l:"^"},"v":{x:"0",y:"1",r:"<",l:">"},"<":{x:"-1",y:"0",l:"v",r:"^"}}
        self.path={"0.0":0}
        self.dir="^"
        self.cur="0.0"


    def move(self,colour,turn):
        self.path[self.cur]=colour
        if turn==0:
            #left
            self.dir=self.dirs[self.dir][l]
        elif turn==1:
            self.dir=self.dirs[self.dir][r]
        else:
            raise ValueError("invalid direction",turn)
        coords=self.cur.split(".")
        x=int(coords[0])+int(self.dirs[self.dir][x])
        y=int(coords[1])+int(self.dirs[self.dir][y])
        self.cur=str(x)+"."+str(y)
        if self.cur not in self.path:
            self.path[self.cur]=0
        return self.path[self.cur]

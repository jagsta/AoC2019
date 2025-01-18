import sys
import intcode

file="input.txt"

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)

print(program)

grid={} # key = x.y, value=0 (wall), 1(space), 2(target)
dirs=[{"^":"n","x":0,"y":-1},{">":"e","x":1,"y":0},{"v":"s","x":0,"y":1},{"<":"w","x":-1,"y":0}]

def try_move(direction,x,y):
    for i in range(4):
        x+=dirs[i]["x"]
        y+=dirs[i]["y"]
        if str(x)+"."+str(y) in grid:
            return grid[str(x)+"."+str(y)]
        else:
            r,result=program.execute([direction])
            print("trying",x,y,"found",result)
            grid[str(x)+"."+str(y)]=result
            if result==0:
                continue
            if result==1:
                result=try_move(0,x,y)
                return result
            if result==2:
                break



found=False
while True:
    result=try_move(0,0,0)
    if result==2:
        print("found oxygen,system")
        break

print(grid)


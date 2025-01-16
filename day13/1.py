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

board={}
while True:
    r,x=program.execute()
    if r==99:
        break
    r,y=program.execute()
    if r==99:
        break
    r,tile=program.execute()
    print(f'x:{x}, y:{y} has tile type {tile}')
    board[str(x)+"."+str(y)]=int(tile)
    if r==99:
        break

total=0
for v in board.values():
    if v==2:
        total+=1

print(total)

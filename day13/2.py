import sys
import intcode
import curses


file="input2.txt"

f=open(file)

code=intcode.GrowingList()
for line in f.readlines():
    for c in line.strip().split(","):
        code.append(int(c))

program=intcode.intcode(code)

print(program)

stdscr = curses.initscr()
print(f'{curses.LINES}')
print(f'{curses.COLS}')
curses.curs_set(0)
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
#
#y=board[], x=board[][]
#initialise board

def render(value):
    if value==0:
        return " "
    elif value==1:
        return "@"
    elif value==2:
        return "#"
    elif value==3:
        return "="
    elif value==4:
        return "O"
    else:
        #raise ValueError(f'unknown sprite id {value}')
        return "?"

ballx=0
batx=0
while True:
    rx,x=program.execute()
    if rx!=1:
        break
    ry,y=program.execute()
    rt,tile=program.execute()
    c = render(tile)
    if c=="O":
        ballx=x
    if c=="=":
        batx=x
    try:
        stdscr.addstr(y,x,c)
        stdscr.refresh()
    except:
        pass

score=0
last=0
delayms=1
din=0
while True:
    if batx>ballx:
        din=-1
    elif batx<ballx:
        din=1
    else:
        din=0
    rx,x=program.execute([din])
    if rx==99:
        break
    ry,y=program.execute()
    if ry==99:
        break
    rt,tile=program.execute()
    if rt==99:
        break
#    print(rx,x,ry,y,rt,tile)
    if x==-1 and y==0:
        score=tile
    else:
#        print(f'x:{x}, y:{y} has tile type {tile}')
        c=render(tile)
        if c=="O":
            ballx=x
        if c=="=":
            batx=x
        try:
            stdscr.addstr(y,x,c)
            stdscr.refresh()
        except:
            pass
    curses.napms(delayms)
    #curses.delay_output(delayms)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

print(score)

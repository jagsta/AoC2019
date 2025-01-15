import sys
import re
from itertools import permutations
import math

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

class planet:
    def __init__(self,x,y,z):
        self.x=int(x)
        self.y=int(y)
        self.z=int(z)
        self.dx=0
        self.dy=0
        self.dz=0
        self.vx=0
        self.vy=0
        self.vz=0
        self.pot=0
        self.kin=0
        self.total=0

    def energy(self):
        self.pot=abs(self.x)+abs(self.y)+abs(self.z)
        self.kin=abs(self.vx)+abs(self.vy)+abs(self.vz)
        self.total=self.pot*self.kin

    def deltas(self):
        self.dx+=self.vx
        self.dy+=self.vy
        self.dz+=self.vz

    def __str__(self):
        return f'x:{self.x} vx:{self.vx}\ny:{self.y} vy:{self.vy}\nz:{self.z} vz:{self.vz}'


planets=[]
for line in f.readlines():
   match=re.match(r'<x=(.+), y=(.+), z=(.+)>',line.strip())
   if match:
       x=match.group(1)
       y=match.group(2)
       z=match.group(3)
       planets.append(planet(x,y,z))

for p in planets:
    print(p)

t=0
endt=1000000
interval=endt
pairs=[]
for i,p in enumerate(planets[:-1]):
    for p2 in planets[i+1:]:
        pairs.append([p,p2])
zeros=[None,None,None]
print(len(pairs))
#pairs=list(permutations(planets,2))
while True:
    if t==endt:
        break
    for p in pairs:
        if p[0].x>p[1].x:
            p[0].vx-=1
            p[1].vx+=1
        elif p[0].x<p[1].x:
            p[0].vx+=1
            p[1].vx-=1
        if p[0].y>p[1].y:
            p[0].vy-=1
            p[1].vy+=1
        elif p[0].y<p[1].y:
            p[0].vy+=1
            p[1].vy-=1
        if p[0].z>p[1].z:
            p[0].vz-=1
            p[1].vz+=1
        elif p[0].z<p[1].z:
            p[0].vz+=1
            p[1].vz-=1
    zeropoint=[True,True,True]
    for p in planets:
        p.deltas()
        if p.vx!=0:
            p.x = p.x+p.vx
            zeropoint[0]=False
        if p.vy!=0:
            p.y = p.y+p.vy
            zeropoint[1]=False
        if p.vz!=0:
            p.z = p.z+p.vz
            zeropoint[2]=False
    t+=1
    if zeropoint[0]:
        print(f'vx zeropoint at {t}, p0dx={planets[0].dx}, p1dx={planets[1].dx}, p2dx={planets[2].dx}, p3dx={planets[3].dx}')
        if zeros[0] is None and planets[0].dx==0 and planets[1].dx == 0 and planets[2].dx == 0 and planets[3].dx==0:
            zeros[0]=t
    if zeropoint[1]:
        print(f'vy zeropoint at {t}, p0dy={planets[0].dy}, p1dy={planets[1].dy}, p2dy={planets[2].dy}, p3dy={planets[3].dy}')
        if zeros[1] is None and planets[0].dy==0 and planets[1].dy == 0 and planets[2].dy == 0 and planets[3].dy==0:
            zeros[1]=t
    if zeropoint[2]:
        print(f'vz zeropoint at {t}, p0dz={planets[0].dz}, p1dz={planets[1].dz}, p2dz={planets[2].dz}, p3dz={planets[3].dz}')
        if zeros[2] is None and planets[0].dz==0 and planets[1].dz == 0 and planets[2].dz == 0 and planets[3].dz==0:
            zeros[2]=t
    if t % interval==0:
        print(f'after {t} steps:')
        for p in planets:
            p.energy()
            print(f'pos=<x={p.x}, y={p.y}, z={p.z}>, vel=<x={p.vx}, y={p.vy}, z={p.vy}>')
        print()

print(f'Sum of total energy: {planets[0].total}+{planets[1].total}+{planets[2].total}+{planets[3].total} = {planets[0].total+planets[1].total+planets[2].total+planets[3].total}')
print(f'lcm of {zeros[0],zeros[1],zeros[2]} is {math.lcm(zeros[0],zeros[1],zeros[2])}')

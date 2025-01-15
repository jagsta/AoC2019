import sys
import re
from itertools import permutations

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

class planet:
    def __init__(self,x,y,z):
        self.x=int(x)
        self.y=int(y)
        self.z=int(z)
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

interval=1000
t=0
endt=1000
pairs=[]
for i,p in enumerate(planets[:-1]):
    for p2 in planets[i+1:]:
        pairs.append([p,p2])

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
    for p in planets:
        p.x = p.x+p.vx
        p.y = p.y+p.vy
        p.z = p.z+p.vz
    t+=1
    if t % interval==0:
        print(f'after {t} steps:')
        for p in planets:
            p.energy()
            print(f'pos=<x={p.x}, y={p.y}, z={p.z}>, vel=<x={p.vx}, y={p.vy}, z={p.vy}>')
        print()

print(f'Sum of total energy: {planets[0].total}+{planets[1].total}+{planets[2].total}+{planets[3].total} = {planets[0].total+planets[1].total+planets[2].total+planets[3].total}')

import sys
import math

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)


asteroids={}
y=0
for line in f.readlines():
    x=0
    for c in line.strip():
        if c=="#":
            #asteroid at this coordinate
            asteroids[str(x)+"."+str(y)]=0
        x+=1
    y+=1

print(asteroids)
for asteroid in asteroids:
    for target in asteroids:
        a=asteroid.split(".")
        ax=int(a[0])
        ay=int(a[1])
        t=target.split(".")
        tx=int(t[0])
        ty=int(t[1])
        dx=tx-ax
        dy=ty-ay
        gcd=math.gcd(dx,dy)
        if gcd>1:
            for x in range(0,dx,gcd):
                for y in range(0,dy,gcd):
                    if str(x)+"."+str(y) in asteroids:
                        print("asteroid blocks LoS at",x,y)
            print(asteroid,"has common denominator with",target,": dx dy gcd=",dx,dy,gcd)

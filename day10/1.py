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
        if target==asteroid:
            continue
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
#            print(asteroid,"has common denominator with",target,": dx dy gcd=",dx,dy,gcd)
            ix=dx//gcd
            iy=dy//gcd
            x=ax+ix
            y=ay+iy
            blocked=0
            while True:
                if str(x)+"."+str(y)==asteroid:
                    continue
                elif str(x)+"."+str(y)==target:
                    break
                elif str(x)+"."+str(y) in asteroids:
                    blocked=1
#                    print("asteroid blocks LoS at",x,y)
                    break
                else:
                    x+=ix
                    y+=iy
            if blocked==0:
                asteroids[asteroid]+=1
#                print(asteroid,"to",target,"is NOT blocked, count is:",asteroids[asteroid])
#            else:
#                print(asteroid,"to",target,"is blocked, count is:",asteroids[asteroid])

        else:
            asteroids[asteroid]+=1
#            print(asteroid,"to",target,"does not intersect any other grid location, count is:",asteroids[asteroid])
for v in sorted(asteroids, key=asteroids.get):
    print(v, asteroids[v])

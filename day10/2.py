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
destruct={}
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
                if asteroid not in destruct:
                    destruct[asteroid]={}
                if dx==0:
                    if dy<0:
                        destruct[asteroid][target]=0.0
                    elif dy>0:
                        destruct[asteroid][target]=180.0
                elif dy==0:
                    if dx>0:
                        destruct[asteroid][target]=90.0
                    elif dx<0:
                        destruct[asteroid][target]=270.0
                else:
                    if dx>0 and dy>0:
                        offset=90.0
                    elif dx<0 and dy>0:
                        offset=180.0
                    elif dx<0 and dy<0:
                        offset=270.0
                        d=dx
                        dx=dy
                        dy=d
                    else:
                        offset=0
                    destruct[asteroid][target]=offset+math.degrees(math.atan(abs(dx/dy)))
                    print(asteroid,target,dx,dy,destruct[asteroid][target])
#                print(asteroid,"to",target,"is NOT blocked, count is:",asteroids[asteroid])
#            else:
#                print(asteroid,"to",target,"is blocked, count is:",asteroids[asteroid])

        else:
            asteroids[asteroid]+=1
            if asteroid not in destruct:
                destruct[asteroid]={}
            if dx==0:
                if dy<0:
                    destruct[asteroid][target]=0.0
                elif dy>0:
                    destruct[asteroid][target]=180.0
            elif dy==0:
                if dx>0:
                    destruct[asteroid][target]=90.0
                elif dx<0:
                    destruct[asteroid][target]=270.0
            else:
                if dx>0 and dy>0:
                    offset=90.0
                elif dx<0 and dy>0:
                    offset=180.0
                elif dx<0 and dy<0:
                    offset=270.0
                    d=dx
                    dx=dy
                    dy=d
                else:
                    offset=0.0
                destruct[asteroid][target]=offset+math.degrees(math.atan(abs(dx/dy)))
                print(asteroid,target,dx,dy,destruct[asteroid][target])
#            print(asteroid,"to",target,"does not intersect any other grid location, count is:",asteroids[asteroid])
v=sorted(asteroids, key=asteroids.get)[-1]
print(v, asteroids[v])
i=1
answer=0
for d in sorted(destruct[v], key=destruct[v].get):
    print(i,d, destruct[v][d])
    if i==200:
        coords=d.split(".")
        answer=(int(coords[0])*100)+int(coords[1])
    i+=1

print("answer is",answer)

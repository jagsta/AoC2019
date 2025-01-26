import sys
import re
from collections import defaultdict
import functools

file="input.txt"
decksize=10007
targetcard=2019

if len(sys.argv)>1:
    file=sys.argv[1]

if len(sys.argv)>2:
    decksize=int(sys.argv[2])

if len(sys.argv)>3:
    targetcard=int(sys.argv[3])

f=open(file)

cpos=targetcard

#Happy this is correct 99%
@functools.cache
def bigdeal(cpos,increment):
    newpos=cpos*increment%decksize
    return newpos

def deal(deck,increment):
    tempdeck=deck.copy()
    i=0
    for c in range(decksize):
        tempdeck[i]=deck[c]
        i+=increment
        if i>decksize-1:
            i-=decksize
    return tempdeck

@functools.cache
def bigcut(cpos,position):
    if position>0:
        if cpos<position:
            return decksize-position+cpos
        else:
            return cpos-position
    else:
        if cpos<decksize+position:
            return (cpos-position)%decksize
        else:
            return cpos-(decksize+position)

def cut(deck,position):
    tempdeck=deck.copy()
    if position<0:
        i=decksize+position
    else:
        i=position
    for c in range(0,i):
        tempdeck[decksize-i+c]=deck[c]
    for c in range(i,decksize):
        tempdeck[c-i]=deck[c]
    return tempdeck

@functools.cache
def bigstack(cpos):
    return decksize-1-cpos

def stack(deck):
    tempdeck=deck.copy()
    for i in range(decksize):
        tempdeck[i]=deck[decksize-1-i]
    return tempdeck

shuffle=[]
for line in f.readlines():
    shuffle.append(line.strip())

iterations=101741582076661

posset=set()
posset.add(cpos)
for repeats in range(iterations):
    for cmd in range(len(shuffle)):
        line=shuffle[cmd]
        match=re.match(r'deal with increment (\d+)',line)
        if match:
#            print(line,"deal",match.group(1))
            cpos=bigdeal(cpos,int(match.group(1)))
        match=re.match(r'cut (-*\d+)',line)
        if match:
#            print(line,"cut",match.group(1))
            cpos=bigcut(cpos,int(match.group(1)))
        match=re.match(r'deal into new stack',line)
        if match:
#            print(line,"stack")
            cpos=bigstack(cpos)
#        print(f'current position:{cpos}')
##    print(repeats,cpos)
    if cpos in posset:
        print(f'collision after {repeats}:{cpos}')
        break
    else:
        posset.add(cpos)
    if repeats%1000==0:
        print(repeats)

print(cpos)

## Jeez
# I can combine two sequential operations of the same type
# I can swap the order of two commands
# So I should be able to collect all oprations of the same type together contiguously then combine them all into one operation
#
# That will reduce the shuffle to 3 statements
# Each iteration is those 3 statemnts
# So I can reduce iterations in the same way, to end up with 3 operations which
# replicate the entire set of iterations

# Then I can apply those in reverse, tracking position 2020 to work out what position it started in, and therefore it's value

# Easy! :)
# Rules are in the testing.txt file
import sys
import re
from collections import defaultdict
import functools

file="input.txt"
decksize=10007
targetcard=2019
iterations=1

if len(sys.argv)>1:
    file=sys.argv[1]

if len(sys.argv)>2:
    decksize=int(sys.argv[2])

if len(sys.argv)>3:
    targetcard=int(sys.argv[3])

if len(sys.argv)>4:
    iterations=int(sys.argv[4])

f=open(file)

cpos=targetcard

def rdeal(cpos,increment):
    while True:
        if cpos%increment!=0:
            cpos+=decksize
        else:
            break
    return cpos//increment

def rcut(cpos,position):
    position*=-1
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

def rstack(cpos,ignore):
    return decksize-1-cpos

shuffle=[]
for line in f.readlines():
    match=re.match(r'deal with increment (\d+)',line)
    if match:
#            print(line,"deal",match.group(1))
        shuffle.append((rdeal,int(match.group(1))))
        #cpos=bigdeal(cpos,int(match.group(1)))
    match=re.match(r'cut (-*\d+)',line)
    if match:
#            print(line,"cut",match.group(1))
        shuffle.append((rcut,int(match.group(1))))
#        cpos=bigcut(cpos,int(match.group(1)))
    match=re.match(r'deal into new stack',line)
    if match:
#            print(line,"stack")
        #cpos=bigstack(cpos)
        shuffle.append((rstack,None))
shuffle.reverse()

posset={}
for repeats in range(iterations):
    for line in shuffle:
        #print (f'current position:{cpos}')
        #print(line)
        cpos=line[0](cpos,line[1])
    if cpos in posset:
        raise ValueError(f'collision after {repeats}:{cpos} originally seen at end of iteration {posset[cpos]}')
    else:
        posset[cpos]=repeats
    if repeats%1000==0:
        print(repeats)

print(cpos)

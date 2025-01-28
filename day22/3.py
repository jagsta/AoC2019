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

def switch_rules(rule1,rule2):
    if rule1[0]==rcut:
        if rule2[0]==rdeal:
            return [(rdeal,rule1[1]),(rcut,(rule1[1]*rule2[1])%decksize)]
        elif rule2[0]==rstack:
            return [(rstack,None),(rcut,decksize-rule1[1])]
    elif rule1[0]==rdeal:
        if rule2[0]==rcut:
            return [(rcut,decksize-((rule1[1]*rule2[1])%decksize)),(rdeal,rule1[1])]
        elif rule2[0]==rstack:
            return [(rstack,None),(rdeal,rule1[1]),(rcut,decksize+1-rule1[1])]
    elif rule1[0]==rstack:
        if rule2[0]==rcut:
            return [(rcut,decksize-rule2[1]),(rstack,None)]
        elif rule2[0]==rdeal:
            return [(rdeal,rule2[1]),(rstack,None),(rcut,rule2[1]-1)]

def sort_rules(rule1,rule2):
    if rule1[0]==rcut:
        if rule2[0]==rdeal:
            return [(rdeal,rule2[1]),(rcut,(rule1[1]*rule2[1])%decksize)]
        elif rule2[0]==rstack:
            return [(rstack,None),(rcut,decksize-rule1[1])]
    elif rule1[0]==rdeal:
#        if rule2[0]==rcut:
#            return [(rcut,decksize-((rule1[1]*rule2[1])%decksize)),(rdeal,rule1[1])]
        if rule2[0]==rstack:
            return [(rstack,None),(rdeal,rule1[1]),(rcut,decksize+1-rule1[1])]
#    elif rule1[0]==rstack:
#        if rule2[0]==rcut:
#            return [(rcut,decksize-rule2[1]),(rstack,None)]
#        elif rule2[0]==rdeal:
#            return [(rdeal,rule2[1]),(rstack,None),(rcut,rule2[1]-1)]
    return [rule1,rule2]


def rdeal(cpos,increment):
    print(cpos,increment)

    return (cpos*pow(increment,-1,decksize))%decksize

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

sortedrules=shuffle.copy()

# reorder to contiguous operations
def reorder(rules):
    while True:
        reordered=0
        bottom=len(rules)-1
        for i in range(0,bottom):
            rule1=rules[i]
            rule2=rules[i+1]
            if rule1[0]!=rule2[0]:
                print(f'swapping {rule1} for {rule2}')
                neworder=sort_rules(rule1,rule2)
                rules[i]=neworder[0]
                rules[i+1]=neworder[1]
                if len(neworder)>2:
                    rules.insert(i+2,neworder[2])
                reordered+=1
        if reordered<3:
            break
    return rules

# consolidate
def consolidate(rules):
    temprules=[]
    rule1=rules[0]
    stackcount=0
    for i in range(len(rules)-1):
        rule2=rules[i+1]
        if rule1[0]==rstack:
            stackcount+=1
        if rule1[0]==rule2[0]:
            if rule1[0]==rcut:
                rule1=(rcut,(rule1[1]+rule2[1])%decksize)
            elif rule1[0]==rdeal:
                rule1=(rdeal,(rule1[1]*rule2[1])%decksize)
        if i+1==len(rules)-1:
            temprules.append(rule1)
        if rule1[0]!=rule2[0]:
            if rule1[0]==rstack and stackcount%2==0:
                print(f'even number of stack rules, no stacks in reduced set')
            else:
                temprules.append(rule1)
            rule1=rules[i+1]
            continue
    return temprules

sortedrules=reorder(sortedrules)
sortedrules=consolidate(sortedrules)

for rule in sortedrules:
    print(rule)


#phew, I now have a 3 element ruleset which represents 1 iteration.
# I need to double it, order, consolidate, repeatedly - 2,4,8,16,32...
# for each consolidated list which represents a power of two factor of the number of iterations, add to the final ruleset, then repeat the ordering, consolidation a final time

def powersoftwo(x):
    powers = []
    i = 1
    while i <= x:
        if i & x:
            powers.append(i)
        i <<= 1
    return powers

powers=powersoftwo(iterations)
#powers=powersoftwo(101741582076661)
print(powers)

power=0
finalrules=[]
currentrules=sortedrules.copy()
while True:
    if 2**power in powers:
        print(f'adding 2^{power} copies of ruleset')
        finalrules+=currentrules
    if 2**power > powers[-1]:
        break
    power+=1
    currentrules+=currentrules
    currentrules=reorder(currentrules)
    currentrules=consolidate(currentrules)

for rule in finalrules:
    print(rule)

finalrules=reorder(finalrules)
finalrules=consolidate(finalrules)

print("Final rule set is:")
for rule in finalrules:
    print(rule)

finalrules.reverse()
print("Reverse rule set is:")
for rule in finalrules:
    print(rule)

for line in finalrules:
    cpos=line[0](cpos,line[1])

print(cpos)

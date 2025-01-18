import sys
import re
import functools

class reaction:
    def __init__(self,quantity):
        self.quantity=int(quantity)
        self.needs={}

    def __str__(self):
        return f'{self.quantity} needs: {self.needs}'

file="input.txt"

if len(sys.argv)>1:
    file=sys.argv[1]

f=open(file)

reactions={}
for line in f.readlines():
    #Parse the reactions into a tree/graph
    match=re.findall(r'(\d+ \w+)',line.strip())
    print(line.strip())
    product=match.pop().split(" ")
    if product[1] not in reactions:
        reactions[product[1]]=reaction(product[0])
    for m in match:
        ing=m.split(" ")
        reactions[product[1]].needs[ing[1]]=int(ing[0])

for r in reactions:
    print(r,":",reactions[r].quantity, reactions[r].needs)

ore=0
remains={}
@functools.cache
def process(material,quantity):
    q=0
    #first, how many batches do we need (quantity/material.quantity)
    #how many do we already have? (check quantities dict)
    #how many remaining do we need?
    #for each ingredient, if it exists in reactions(i.e. is not ORE) recurse with n x quantity req'd where n=remaining/batch size, rounded up
    if material in reactions:
        if material in remains:
#            print("we have",remains[material],"already")
            batches=-(-(quantity-remains[material]) // reactions[material].quantity) # janky way to round up
            remains[material]+=(batches*reactions[material].quantity) - quantity
        else:
            batches=-(-quantity // reactions[material].quantity) # janky way to round up
            remains[material]=(batches*reactions[material].quantity) - quantity
#        print(batches,"batches of",material,"required, remainder",remains[material])


        for m in reactions[material].needs:
#            print("we need",-(-batches*reactions[material].needs[m]),m)
            q+=process(m,-(-batches*reactions[material].needs[m]))
        return q
    else:
        return quantity

totalore=1000000000000
ticksize=8
marker=0

while True:
    ticks = 10**ticksize
    marker+=ticks
    ore=process("FUEL",marker)
    print("Trying",marker,": requires",ore,"ore")
    if totalore<ore:
        #we overshot, back off by one tick and reduce tick size
        marker-=ticks
        ticksize-=1
    elif totalore==ore:
        #Jeez that was lucky
        break
    if ticksize<0:
        #we're into fractions of FUEL, give up
        break

print("Maximum possible fuel we can produce with",totalore,"is",marker,"units")

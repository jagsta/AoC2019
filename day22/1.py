import sys
import re

file="input.txt"
decksize=10007

if len(sys.argv)>1:
    file=sys.argv[1]

if len(sys.argv)>2:
    decksize=int(sys.argv[2])

f=open(file)

deck={}
for i in range(decksize):
    deck[i]=i

def deal(deck,increment):
    tempdeck=deck.copy()
    i=0
    for c in range(decksize):
        tempdeck[i]=deck[c]
        i+=increment
        if i>decksize-1:
            i-=decksize
    return tempdeck


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

def stack(deck):
    tempdeck=deck.copy()
    for i in range(decksize):
        tempdeck[i]=deck[decksize-1-i]
    return tempdeck

for line in f.readlines():
    match=re.match(r'deal with increment (\d+)',line)
    if match:
        print(line,"deal",match.group(1))
        deck=deal(deck,int(match.group(1)))
    match=re.match(r'cut (-*\d+)',line)
    if match:
        print(line,"cut",match.group(1))
        deck=cut(deck,int(match.group(1)))
    match=re.match(r'deal into new stack',line)
    if match:
        print(line,"stack")
        deck=stack(deck)
    print(f'current position:{list(deck.keys())[list(deck.values()).index(2019)]}')

s=""
for i in range(decksize):
    s+=str(deck[i])+","
print(s[:-1])
print(list(deck.keys())[list(deck.values()).index(2019)])

import sys
from terran import *
Timeout = int(sys.argv[2])
KeyUnit = sys.argv[1]
#Timeout = 330
simulator = terran(Timeout)

from commands import getoutput as gop

output = gop('cat ./terranbuilds/%s%s.dat | grep -m 1 "|"' % (KeyUnit, Timeout)).split('\n')[0].split('|')
#if output[0] == '':
    #output = gop('cat Marauder%s.dat | grep -m 1 "-"' % Timeout).split('-')



Q = []
i = 0
for item in output:
    i += 1
    Q.append((i, Item(globals()[item], simulator)))
P = pipeline(Q)

simulator.evaluate(P)


from RBUT import *
from zerg import *
import time,sys

oldStdout = sys.stdout
sys.stdout = open("NoExtractor.log", "w")

T = 0.
m = []
t = []
simulator = zerg(0.5)
PriorityQueue = []
#def condition1():
   #return  simulator.population - simulator.PopOcupied >= Drone.PopReq
def condition2():
   return  simulator.mineral > 100.
#PriorityQueue.append((1,ConditionItem(Drone, simulator, condition1)))
PriorityQueue.append((1,NumberItem(Drone, simulator, 3)))
#PriorityQueue.append((2,ConditionItem(NumberItem(Extractor, simulator, 2), simulator, condition2)))
#PriorityQueue.append((4,CancelItem(Extractor, simulator)))
#PriorityQueue.append((5,CancelItem(Extractor, simulator)))
PriorityQueue.append((3,NumberItem(Overlord, simulator, 1)))
PriorityQueue.append((4,NumberItem(Drone, simulator, 1)))
PriorityQueue.append((6,NumberItem(Drone, simulator, 3)))
PriorityQueue.append((8,NumberItem(Spawning_Pool,simulator, 1)))
PriorityQueue.append((9,NumberItem(Drone, simulator, 4)))
PriorityQueue.append((10,NumberItem(Queen, simulator, 1)))
PriorityQueue.append((11,NumberItem(Overlord, simulator, 1)))
PQ = pipeline(PriorityQueue)

def run(simulator, m, t):
    m.append(simulator.mineral) 
    t.append(simulator.time)
    PQ.make()
    m.append(simulator.mineral) 
    t.append(simulator.time)
    m.append(simulator.mineral) 
    t.append(simulator.queue[0][0])

print Hatchery.__class__
Hatchery.run()
simulator.Mining()
simulator.mainloop(200., run, simulator, m, t)

for log in simulator.log:
    print '%s: %s took %s' % (log[0].name, log[2], log[3])

import matplotlib
import matplotlib.pyplot as plt
from numpy import array
from plot import *

fig = plt.figure()
sp = fig.add_subplot(111)
plt.xlabel('Time (s)')
plt.ylabel('Mineral')
for item in simulator.log:
    plotlog(sp,item)
plt.plot(t, m)
plt.show()

sys.stdout = oldStdout

import RBUT 
from zerg import *
import time,sys

oldStdout = sys.stdout
sys.stdout = open("Cancel1Extractor.log", "w")


T = 0.
m = []
t = []
simulator = zerg(0.5)
PriorityQueue = []
#def condition1():
   #return  simulator.population - simulator.PopOcupied >= Drone.PopReq
def condition2():
   return  simulator.mineral > 75.
Cancel1Extractor = RBUT.Combo([ (1, RBUT.NumberItem(Extractor, simulator, 1)), (2, RBUT.NumberItem(Drone, simulator, 1)), (3,RBUT.CancelItem(Extractor, simulator)) ])
PriorityQueue.append((1,RBUT.NumberItem(Drone, simulator, 4)))
PriorityQueue.append((2,RBUT.ConditionItem(Cancel1Extractor, simulator, condition2)))
PriorityQueue.append((3,RBUT.NumberItem(Overlord, simulator, 1)))
PriorityQueue.append((4,RBUT.NumberItem(Drone, simulator, 2)))
PriorityQueue.append((5,RBUT.NumberItem(Spawning_Pool,simulator, 1)))
PriorityQueue.append((6,RBUT.NumberItem(Drone, simulator, 4)))
PriorityQueue.append((7,RBUT.NumberItem(Queen, simulator, 1)))
PriorityQueue.append((8,RBUT.NumberItem(Overlord, simulator, 1)))
PriorityQueue.append((9,RBUT.NumberItem(Zergling, simulator, 'IDF')))
PQ = RBUT.pipeline(PriorityQueue)

def run(simulator, m, t):
    m.append(simulator.mineral) 
    t.append(simulator.time)
    PQ.make()
    m.append(simulator.mineral) 
    t.append(simulator.time)
    m.append(simulator.mineral) 
    t.append(simulator.queue[0][0])

#Hatchery.hatching()
Hatchery.run()
#simulator.Mining()
simulator.mainloop(300., run, simulator, m, t)
Hatchery.StopHatch()

for log in simulator.log:
    print '%s: %s took %s' % (log[0].name, log[2], log[3])

import matplotlib
import matplotlib.pyplot as plt
from numpy import array
from plot import *

fig = plt.figure()
sp = fig.add_subplot(111)
for item in simulator.log:
    plotlog(sp,item)
plt.xlabel('Time (s)')
plt.ylabel('Mineral')
plt.plot(t, m)
plt.show()

sys.stdout = oldStdout

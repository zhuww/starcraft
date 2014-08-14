from zerg import *
from Control import *
import time,sys

oldStdout = sys.stdout
sys.stdout = open("10Pool.log", "w")

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
PriorityQueue.append((1,NumberItem(Drone, simulator, 4)))
#PriorityQueue.append((2,ConditionItem(NumberItem(Extractor, simulator, 2), simulator, condition2)))
#PriorityQueue.append((4,CancelItem(Extractor, simulator)))
#PriorityQueue.append((5,CancelItem(Extractor, simulator)))
PriorityQueue.append((2,NumberItem(Spawning_Pool,simulator, 1)))
PriorityQueue.append((3,NumberItem(Overlord, simulator, 1)))
PriorityQueue.append((6,NumberItem(Drone, simulator, 5)))
PriorityQueue.append((7,NumberItem(Queen, simulator, 1)))
PriorityQueue.append((8,NumberItem(Overlord, simulator, 1)))
PriorityQueue.append((8,NumberItem(Zergling, simulator, 'IDF')))
PQ = pipeline(PriorityQueue)


def run(simulator, m, t):
    m.append(simulator.mineral) 
    t.append(simulator.time)
    PQ.make()
    m.append(simulator.mineral) 
    t.append(simulator.time)
    #m.append(simulator.mineral) 
    #t.append(simulator.queue[0][0])

Hatchery.run()
#simulator.Mining()
simulator.mainloop(200., run, simulator, m, t)

for log in simulator.log:
    print '%s: %s took %s' % (log[0].name, log[2], log[3])

import matplotlib
import matplotlib.pyplot as plt
from numpy import array
from plot import *

fig = plt.figure()
sp = fig.add_subplot(111)
#sp.set_xlim(0,200)
#sp.set_ylim(0,600)
for item in simulator.log:
    plotlog(sp,item)
plt.xlabel('Time (s)')
plt.ylabel('Mineral')
plt.plot(t, m)
plt.show()

sys.stdout = oldStdout

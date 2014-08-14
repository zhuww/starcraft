from RBUT import *
from zerg import *
from Build import *
import time,sys

#oldStdout = sys.stdout
#sys.stdout = open("Cancel1Extractor.log", "w")


T = 0.
m = []
g = []
t = []
simulator = zerg(0.5)

#build = Cancel1Extractor(simulator, 90.)
#build = Cancel2Extractor(simulator, 90.)
#build = NoExtractor(simulator, 80.)
#build = RoachBuild(simulator, 145.)
#build = BanelingRush(simulator, 90.)
build = TwoBase(simulator, 140.)

def run(simulator, m, g, t):
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.time)
    build.make()
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.time)
    #m.append(simulator.mineral) 
    #g.append(simulator.gas) 
    #t.append(simulator.queue[0][0])

Hatchery.run()
#simulator.Mining()
simulator.mainloop(300., run, simulator, m, g, t)
print 'by 5min, %i Zerglings were produced.' % Zergling.number
#print 'by 5min, %i Roachs were produced.' % Roach.number
#print 'by 5min, %i Banelings were produced.' % Baneling.number
print 'by 5min, %i Drone were produced.' % Drone.number

for log in simulator.log:
    #if log[0] == Lair:
    if log[0] == Hatchery:
        print (log[2]+log[3], Drone.number)

import matplotlib
import matplotlib.pyplot as plt
from numpy import array
from plot import *

fig = plt.figure()
sp = fig.add_subplot(111)
for item in simulator.log:
    plotlog(sp,item)
plt.xlabel('Time (s)')
plt.ylabel('Mineral, Gas')
plt.plot(t, m)
plt.plot(t, g, color='red')
plt.show()

#sys.stdout = oldStdout

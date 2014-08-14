#from RBUT import *
#from zerg import *
from terran import *
from tools import *
#from Build import *

#Supply_Depot.__class__ = Housecls
#print type(Supply_Depot)

def MoreSCVs(simulator, t):
    Q = []
    #Q.append((1,NumberItem(SCV, simulator, 'IDF')))
    Q.append((1,NumberItem(SCV, simulator, 3)))
    Q.append((2,NumberItem(Supply_Depot, simulator,1)))
    Q.append((3,NumberItem(SCV, simulator, 2)))
    Q.append((4,NumberItem(Barracks, simulator, 2)))
    Q.append((5,NumberItem(SCV, simulator, 5)))
    Q.append((6,Item(Orbital_Command, simulator)))
    PQ = pipeline(Q)
    return workflow([PQ])
        
    #print TestBuild(MoreSCVs, SCV, SCV)


T = 0.
m = []
g = []
t = []
simulator = terran(0.5)

build = MoreSCVs(simulator, 140.)

def run(simulator, m, g, t):
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.time)
    build.make()
    print simulator.population
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.time)
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.queue[0][0])

#Hatchery.run()
simulator.Mining()
simulator.mainloop(120., run, simulator, m, g, t)
#print 'by 5min, %i Zerglings were produced.' % Zergling.number
#print 'by 5min, %i Roachs were produced.' % Roach.number
#print 'by 5min, %i Banelings were produced.' % Baneling.number
#print 'by 5min, %i Drone were produced.' % Drone.number
print 'by 2min, %i SCVs were produced.' % SCV.number


#for log in simulator.log:
    #if log[0] == Hatchery:
        #print (log[2]+log[3], Drone.number)

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

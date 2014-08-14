import RBUT 
from zerg import *
import time,sys
T = 0.
m = []
t = []
#Overlordmade = False
simulator = zerg(0.5)
#simulator.Mining()
#Hatchery.hatching()
#while T <= 10:
    #M = simulator.mineral
    #m.append(M) 
    #simulator.make(Drone)
    #if  simulator.population-simulator.PopOcupied == 0 and M > Overlord.MineReq:
    #if  simulator.population-simulator.PopOcupied == 0 and M > Spawning_Pool.MineReq:
        #if not Overlordmade:
            #simulator.make(Overlord)
            #simulator.build(Spawning_Pool)
            #Overlordmade = True
    #elif simulator.population > simulator.PopOcupied:
        #Overlordmade = False
    #if Drone.number > simulator.MineralMiner:
        #simulator.MineralMiner = Drone.number
    #time.sleep(0.1)
    #T += 0.1
    #t.append(T)
#simulator.StopMining()
#Hatchery.StopHatch()

def run(simulator, m, t, Overlordmade=[False]):
    M = simulator.mineral
    m.append(M) 
    simulator.make(Drone)
    M = simulator.mineral
    if  not Larva.number == 0 and simulator.population-simulator.PopOcupied == 0 and M > Overlord.MineReq:
        if not Overlordmade[0]:
            print 'try to make Overlord'
            simulator.make(Overlord)
            Overlordmade[0] = True
    elif simulator.population > simulator.PopOcupied:
        Overlordmade[0] = False
    if Drone.number > simulator.MineralMiner:
        simulator.MineralMiner = Drone.number
    t.append(simulator.time)

Hatchery.hatching()
simulator.mainloop(60., run, simulator, m, t)
Hatchery.StopHatch()

import matplotlib
import matplotlib.pyplot as plt
from numpy import array

print len(t), len(m)

t = array(t)
t = t-t[0]

plt.plot(t, m)
plt.show()



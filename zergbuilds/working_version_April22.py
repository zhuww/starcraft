import RBUT 
from zerg import *
import time,sys
T = 0.
m = []
t = []
simulator = zerg(0.5)
def run(simulator, m, t, made=[False] * 3):
    M = simulator.mineral
    m.append(M) 
    t.append(simulator.time)
    if Drone.number < 14:
        simulator.make(Drone)
    if  not Larva.number == 0 and simulator.population-simulator.PopOcupied == 0 and simulator.mineral > Overlord.MineReq:
        if not made[0]:
            print simulator.make(Overlord)
            made[0] = True
    elif simulator.population > simulator.PopOcupied:
        made[0] = False
    if simulator.mineral > Spawning_Pool.MineReq and not made[1]:
        simulator.make(Spawning_Pool)
        made[1] = True
    if simulator.mineral > Queen.MineReq and simulator.population-simulator.PopOcupied == Queen.PopReq and not made[2]:
        simulator.make(Queen)
    if not Queen.number == 0:
        Queen.Spawn_Larva()
    if Drone.number < 16:
        simulator.make(Drone)
    else:
        simulator.make(Hatchery)
    if Drone.number > simulator.MineralMiner:
        simulator.MineralMiner = Drone.number

Hatchery.hatching()
simulator.mainloop(200., run, simulator, m, t)
Hatchery.StopHatch()

import matplotlib
import matplotlib.pyplot as plt
from numpy import array



plt.plot(t, m)
plt.show()



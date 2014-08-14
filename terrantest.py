#from RBUT import *
#from zerg import *
from terran import *
from tools import *
#from Build import *

#Supply_Depot.__class__ = Housecls
#print type(Supply_Depot)

def TwoRax(simulator, t):
    Q = []
    P = [
    (1, SCV),
    (2, SCV),
    (3, SCV),
    (4, SCV),
    (5, Supply_Depot),
    (6, SCV),
    (7, SCV),
    (8, SCV),
    (9, SCV),
    (10, Barracks),
    (11, SCV),
    (12, SCV),
    (13, Orbital_Command),
    (14, Extra_Supplies),
    (15.5, MULE),
    (16, SCV),
    (17, Supply_Depot),
    (18, SCV),
    (19, Marine),
    (20, SCV),
    (21, Marine),
    (22, Marine),
    (23, Barracks_Tech_Lab),
    (24, Supply_Depot),
    (25, Marauder),
    (26, Barracks_Tech_Lab),
    (27, Marine),
    (28, Marauder),
    (29, Marine),
    (30, Marauder),
    (31, Marauder),
    (32, Marauder),
    (33, Barracks)]
    for it in P:
        Q.append((it[0], Item(it[1], simulator)))
    #Q.append((1,Item(Refinery, simulator)))
    #Q.append((1,NumberItem(SCV, simulator, 'IDF')))
    #Q.append((1,NumberItem(SCV, simulator, 4)))
    #Q.append((2,Item(Refinery, simulator)))
    #Q.append((3,Item(Supply_Depot, simulator)))
    #Q.append((4,NumberItem(Barracks, simulator, 2)))
    #Q.append((5,Item(Barracks_Tech_Lab, simulator)))
    #Q.append((6,Item(Marauder, simulator)))
    #Q.append((7,Item(Marine, simulator)))
    #Q.append((8,Item(Marauder, simulator)))
    #Q.append((9,Item(Marine, simulator)))
    #Q.append((10,Item(Marauder, simulator)))
    #Q.append((11,Item(Supply_Depot, simulator)))
    #Q.append((6,Item(Orbital_Command, simulator)))
    #Q.append((7,Item(Barracks, simulator)))
    #Q.append((5.5, NumberItem(Marine, simulator, 4)))
    #Q.append((8,Item(MULE, simulator)))
    #Q.append((9,Item(Barracks_Tech_Lab, simulator)))
    #Q.append((10,Item(Barracks_Tech_Lab, simulator, 5)))
    #Q.append((11, NumberItem(Marauder, simulator, 'IDF')))
    #Q.append((11,Item(Stimpack, simulator)))
    #Q.append((9, NumberItem(SCV, simulator, 5)))
    #Q.append((9,Combo([(1,NumberItem(SCV, simulator, 'IDF')), (2,NumberItem(Marine, simulator, 'IDF'))])))
    PQ = pipeline(Q)
    #q = []
    #q.append((9, TimingItem(DummyItem(simulator), simulator, t+100)))
    #q.append((11, NumberItem(Marine, simulator, 'IDF')))
    #SQ = pipeline(q)
    #return workflow([PQ, SQ])
    return workflow([PQ])
        
    #print TestBuild(TwoRax, SCV, SCV)
#print Marine.BuildingBusy, Marine.BuildingReq
#import sys
#sys.exit(0)



T = 0.
m = []
g = []
t = []
simulator = terran(460)
#simulator.restart()

print Extra_Supplies.number

build = TwoRax(simulator, 80)

def run(simulator, m, g, t):
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.time)
    build.make()
    m.append(simulator.mineral) 
    g.append(simulator.gas) 
    t.append(simulator.time)
    #if Barracks_Tech_Lab.number > 0:
        #print Barracks.List
    #print Barracks.number
    if Orbital_Command.number > 0:
        print 'Orbital_Command', Orbital_Command.List[0]
    #print simulator.population, simulator.PopOcupied
    #print simulator.Miner, simulator.GasMiner
    #print Command_Center.number, Command_Center.occupied
    #print Barracks.number, Barracks.occupied
    #m.append(simulator.mineral) 
    #g.append(simulator.gas) 
    #t.append(simulator.queue[0][0])

#Hatchery.run()
#simulator.Mining()
simulator.mainloop(run, simulator, m, g, t)
#print 'by 5min, %i Zerglings were produced.' % Zergling.number
#print 'by 5min, %i Roachs were produced.' % Roach.number
#print 'by 5min, %i Banelings were produced.' % Baneling.number
#print 'by 5min, %i Drone were produced.' % Drone.number
#print 'by 5min, %i SCVs were produced.' % SCV.number
print 'by 5min, %i Marines were produced.' % Marine.number


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
plt.plot(t, m, color='blue')
plt.plot(t, g, color='red')
plt.show()

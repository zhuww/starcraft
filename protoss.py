from RBUT import *
import RBUT
from collections import deque


class Nexus_class(Nexus.__class__):
    __metaclass__ = Magical 
    def __init__(self, origin):
        RBUT.building.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.BuildingPvd, origin.UnitPvd, origin.TechPvd, origin.BuildingReq)
        self.name = origin.name
        self.health = 750
        self.shield = 750
        self.energy = 0
        self.stats = [1500, 0, 0]

Nexus = Nexus_class(Nexus)
#print Nexus.__dict__

class Chrono_Boost_class(RBUT.things, Item):
    def __init__(self):
        RBUT.things.__init__(self, 0,0,20, )
        self.List = []
    def __call__(self,target):
        if issubclass(self.target.__class__, RBUT.building):
            self.target = target
            self.name = 'Chrono_Boost_'+target.name
        elif issubclass(self.target.__class__, (RBUT.unit, RBUT.tech)):
            self.target = target.BuildingBusy
            self.name = 'Chrono_Boost_'+target.BuildingBusy.name
    def make(self):
        if Nexus.number == 0:
            return False
        if issubclass(self.target.__class__, RBUT.building) and self.target.number == 0:
            #print "Boost target %s does not exist." % self.target.name
            return False 
        if all([Nx[2] < 25 for Nx in Nexus.List]) :
            #print "Chrono_Boost failed because Nexus does not have enough energy"
            #print Nexus.List, Nexus.stats
            return False
        for Nx in Nexus.List:
            if Nx[2] >= 25:
                Nx[2] += -25
                self.build()
                return True
    def creat(self):
        self.number += -1
        self.history += 1
        i = self.threadqueue.popleft()
        if self.s.verbose:
            print '%dm%2.0fs: %s %i broken (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, self.history, self.s.PopOcupied, self.s.population)
    def build(self):
        t = self.s.time + self.TimeReq
        i = len(self.List)+len(self.threadqueue)
        heappush(self.s.queue, [t, [self,i]])
        self.threadqueue.append(i)
        self.s.log.append([self, self.s.mineral, self.s.time, self.TimeReq])
        if self.s.verbose:
            print '%dm%2.0fs: call down %s %i (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, self.history+len(self.threadqueue), self.s.PopOcupied, self.s.population)
        self.number += 1
        return True
Chrono_Boost = Chrono_Boost_class()

allbuildings = [
Nexus,  
Pylon,	
Assimilator ,
Gateway, 
Forge ,
Photon_Cannon ,
Warpgate ,
Cybernetics_Core ,
Twilight_Council ,
Robotics_Facility,
Stargate,
Templar_Archives,
Dark_Shrine ,
Robotics_Bay,
Fleet_Beacon,]

allunits=[
Probe,
Zealot, 
Stalker,
Sentry,
Observer, 
Immortal, 
Warp_Prism, 
Colossus, 
Phoenix, 
Void_Ray,
High_Templar,
Dark_Templar, 
Archon, 
Carrier, 
Mothership, 
Interceptors,
]

alltechs=[
Blink,
Charge,	
Extended_Thermal_Lance,	
Gravitic_Boosters,
Gravitic_Drive,	
Graviton_Catapult,
Hallucination,	
Protoss_Air_Armor_1,
Protoss_Air_Armor_2, 
Protoss_Air_Armor_3,
Protoss_Air_Weapons_1,
Protoss_Air_Weapons_2,
Protoss_Air_Weapons_3,
Protoss_Ground_Armor_1,
Protoss_Ground_Armor_2,	
Protoss_Ground_Armor_3,	
Protoss_Ground_Weapons_1,
Protoss_Ground_Weapons_2, 
Protoss_Ground_Weapons_3, 
Protoss_Shields_1,
Protoss_Shields_2,
Protoss_Shields_3,
Psionic_Storm,	
Warp_Gate,
]


class protoss(RBUT.race):
    def __init__(self, timestep=1.5):
        RBUT.race.__init__(self, 'protoss', timestep)
        self.allbuildings = allbuildings
        self.allunits = allunits
        self.alltechs  = alltechs
        self.startbuildings = [Nexus]
        self.startunits = [(Probe, 6)]
        self.Miner = Probe 
        self.geyser = Assimilator
        self.House = Pylon
        self.InitialPopulation = 10
        self.population = self.InitialPopulation
        self.restart()
    def restart(self):
        RBUT.race.restart(self)
    def CalculateResourse(self, time):
        lapse = time - self.time
        self.mineral += self.mineralrate()*lapse #+ (MULE.number-MULE.occupied)*10./3*lapse
        self.gas += self.GasMiner*0.555555555555555*lapse #112/3/60
        for unit in self.MagicalList:
            for individual in unit.List:
                individual[2] = min(200, individual[2] + 50./90 * lapse)

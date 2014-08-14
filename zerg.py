from RBUT import *
import RBUT
from collections import deque


class ZergHousecls(RBUT.unit):
    def __init__(self, origin):
        RBUT.unit.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.PopReq, origin.UnitReq, origin.NuReq,  BuildingBusy=origin.BuildingBusy, UpgradeFrom=origin.UpgradeFrom)
        self.name = origin.name
    def creat(self):
        RBUT.unit.creat(self)
        self.s.population += 8
Overlord = ZergHousecls(Overlord)

Larva.HatcheryQueue = deque([])
Larva.SpawnQueue = deque([])
def LarvaCount():
    '''Override the Larva.number, to enable control over from which hatcherythe Larva is hatching. '''
    def fget(self):
        return len(self.List)
    def fset(self, value):
        i = value - len(self.List)
        if i > 0:
            if i == 1:
                j = self.HatcheryQueue.popleft()
                HC= Hatchery.HatcheryList[j]
                HC.LarvaNumber+=1
                if HC.LarvaNumber >=3:
                    HC.hatching = False
                else:
                    Larva.HatcheryQueue.append(j)
                    Larva.make()
            elif i == 4:
                j = self.SpawnQueue.popleft()
                HC= Hatchery.HatcheryList[j]
                HC.LarvaNumber+=4
                HC.spawned = False
            self.List+= ([self.stats] * i)
        elif i < 0:
            while i < 0:
                self.List = self.List[:-1]
                Hatchery.decrement()
                i += 1
    return locals()

class Larvacls (Larva.__class__):
    number = property(**LarvaCount())
Larva.__class__ = Larvacls
Larva.verbose = False

class status(object):
    def __init__(self, NLarva=3, hatching=False, spawned=False):
        self.LarvaNumber = NLarva
        self.hatching = hatching
        self.spawned = spawned
class Hatcherycls(RBUT.building):
    def __init__(self, origin):
        RBUT.building.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq,  UnitSpend = None )
        self.name = origin.name
        self.HatcheryList = []
        self.stats = [3000,0,3]
    def creat(self):
        RBUT.building.creat(self)
        self.HatcheryList.append(status())
        self.s.population += 2
        self.s.BaseCount += 1 #
    def run(self):
        self.HatcheryList = []
        for i in range(self.number):
            self.HatcheryList.append(status())
        self.LarvaNumber = sum([x.LarvaNumber for x in self.HatcheryList])
    def decrement(self,N=1):
            Num = 0
            j = -1
            for i in range(self.number):
                HC = self.HatcheryList[i] 
                if HC.hatching:
                    continue
                elif HC.LarvaNumber == 3: 
                    HC.LarvaNumber += -1
                    Larva.HatcheryQueue.append(i)
                    Larva.make()
                    HC.hatching = True
                    return
                else:
                    if HC.LarvaNumber > Num: 
                        Num = HC.LarvaNumber
                        j = i
            if not j == -1: 
                self.HatcheryList[j].LarvaNumber += -1
                Larva.HatcheryQueue.append(j)
                Larva.make()
                self.HatcheryList[j].hatching = True
                return 
            else:
                for i in range(self.number):
                    HC = self.HatcheryList[i] 
                    if HC.LarvaNumber > Num: 
                        Num = HC.LarvaNumber
                        j = i
                if j == -1:return
                self.HatcheryList[j].LarvaNumber += -1
    def StopHatch(self):
        self.go = False
    def inject(self, i):
        class Spawn(object):
            def __init__(self, simulator, i ):
                self.TimeReq = 40
                self.s = simulator
                self.i = i
                self.MineReq = 0
                self.verbose = False
            def creat(self):
                Larva.number+=4
                print '%s: Hatchery Spawned' % self.s.time
            def make(self):
                t = self.s.time + self.TimeReq
                heappush(self.s.queue, [t, [self,self.i]])
                #self.s.log.append([self, self.s.mineral ,self.s.time, self.TimeReq])
                Larva.SpawnQueue.append(i)
                print '%s: Hatchery injected' %self.s.time
        if self.HatcheryList[i].spawned == False:
            self.HatcheryList[i].spawned = True
        else: return False
        Spawn(self.s, i).make()
OldHatchery = Hatchery
Hatchery = Hatcherycls(OldHatchery)
#Lair.UpgradeFrom = Hatchery #Be careful, better leave Hive as another building
Hive.UpgradeFrom = Lair
Greater_Spire.UpgradeFrom = Spire

class QueenEnergy(object):
    def __init__(self, queen, simulator, cooldown):
        self.name = 'Queen spawn Hatchery'
        self.queen = queen
        self.cooldown = cooldown
        self.s = simulator
        self.List = []
        self.threadqueue = deque([])
    def creat(self):
        i = self.threadqueue.popleft() # which queen is this
        self.queen.Spawn_Larva()
        self.make()
    def make(self):
        t = self.s.time + self.cooldown
        i = len(self.List) + len(self.threadqueue)
        heappush(self.s.queue, [t, [self,i]])
        self.threadqueue.append(i)
class Queencls(RBUT.unit):
    '''!!!Unfinished!!!''' 
    __metaclass__ = Magical
    EnergyReq = 25
    cooldown = 45
    def __init__(self, origin):
        RBUT.unit.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.PopReq, origin.UnitReq, origin.NuReq )
        self.name = origin.name
    def creat(self):
        RBUT.unit.creat(self)
        i = self.number
        Energy=QueenEnergy(self,self.s,self.cooldown)
        Energy.threadqueue.append(i)
        Energy.creat()
    def Spawn_Larva(self):
        def FirstOpen(HCList):
            for i in range(len(HCList)):
                if not HCList[i].spawned:return i
            return None
        if not self.number == 0:
            j = FirstOpen(Hatchery.HatcheryList)
            if not j == None:
                Hatchery.inject(j)
        else:pass
Queen = Queencls(Queen)

class ZerglingCls(Zergling.__class__):
    def __init__(self, origin):
        RBUT.unit.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.PopReq, origin.UnitReq, origin.NuReq )
        self.name = origin.name
    def creat(self):
        if self.number == 0:
            self.s.UnitList.append(self)
        self.number += 2
        i = self.threadqueue.popleft()
        if self.verbose:
            print '%.1f s: %s %i created' % (self.s.time, self.name, len(self.List))
Zergling = ZerglingCls(Zergling)



Hatchery.BuildingPvd = [Spawning_Pool, Evolution_Chamber]
Evolution_Chamber.BuildingPvd = [Spore_Crawler]
Spawning_Pool.BuildingPvd = [Lair, Baneling_Nest, Roach_Warren, Spine_Crawler]
Lair.BuildingPvd = [Hydralisk_Den, Spire, Infestation_Pit, Nydus_Network]
Infestation_Pit.BuildingPvd = [ Hive ]
Hive.BuildingPvd = [Ultralisk_Cavern, Greater_Spire]
Hatchery.UnitPvd = [Larva, Drone, Overlord]
Spawning_Pool.UnitPvd = [Zergling,Queen]
Baneling_Nest.UnitPvd = [Baneling]
Lair.UnitPvd = [Overseer]
Roach_Warren.UnitPvd = [Roach]
Hydralisk_Den.UnitPvd = [Hydralisk]
Infestation_Pit.UnitPvd = [Infestor]
Spire.UnitPvd = [Mutalisk, Corruptor]
Nydus_Network.UnitPvd = [Nydus_Worm]
Ultralisk_Cavern.UnitPvd = [Ultralisk]
Greater_Spire.UnitPvd = [Brood_Lord]

allbuildings = [Hatchery, 
        Extractor,
        Evolution_Chamber, 
        Spawning_Pool, 
        Lair, 
        Infestation_Pit, 
        Hive, 
        Evolution_Chamber,
        Spore_Crawler, 
        Spine_Crawler, 
        Roach_Warren, 
        Baneling_Nest, 
        Hydralisk_Den, 
        Spire, 
        Nydus_Network, 
        Ultralisk_Cavern, 
        Greater_Spire]

allunits = [Larva, 
    Drone,
    Overlord,
    Zergling,
    Queen,
    Hydralisk,
    Baneling,
    Overseer,
    Roach,
    Infestor,
    Mutalisk,
    Corruptor,
    Nydus_Worm,
    Ultralisk,
    Brood_Lord,
    Infested_Terran,
    Broodling,
    Changeling]
alltechs = [Organic_Carapace,
    Metabolic_Boost,
    Adrenal_Glands,
    Pneumatized_Carapace,
    Burrow,
    Ventral_Sacs,
    Glial_Reconstitution,
    Tunneling_Claws,
    Grooved_Spines,
    Centrifugal_Hooks,
    Peristalsis,
    Pathogen_Glands,
    Chitinous_Plating,
    Anabolic_Synthesis,
    Missile_Attacks_1,
    Missile_Attacks_2,
    Missile_Attacks_3,
    Melee_Attacks_1,
    Melee_Attacks_2,
    Melee_Attacks_3,
    Ground_Carapace_1,
    Ground_Carapace_2,
    Ground_Carapace_3,
    Flyer_Attack_1,
    Flyer_Attack_2,
    Flyer_Attack_3,
    Flyer_Carapace_1,
    Flyer_Carapace_2,
    Flyer_Carapace_3,]


for building in allbuildings:
    building.UnitSpend = Drone
    for sons in building.BuildingPvd:
        sons.BuildingReq.append(building)
    for unit in building.UnitPvd:
        unit.BuildingReq.append(building)

for unit in allunits[1:-3]:
    unit.UnitReq = Larva
    unit.NuReq = 1
#exceptions
Baneling.UpgradeFrom = Zergling
Brood_Lord.UpgradeFrom = Corruptor
Lair.BuildingReq.append(Queen)


class zerg(RBUT.race):
    def __init__(self, timestep=1.5):
        RBUT.race.__init__(self, 'zerg', timestep)
        self.allbuildings = allbuildings
        self.allunits = allunits
        self.alltechs  = alltechs
        self.startbuildings = [Hatchery]
        self.startunits = [(Larva, 3), (Drone, 6), (Overlord, 1)]
        self.Miner = Drone
        self.geyser = Extractor
        self.House = Overlord
        Larva.HatcheryQueue = deque([])
        self.restart()

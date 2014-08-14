from RBUT import *
import RBUT
from collections import deque

class Command_Center_class(Command_Center.__class__):
    def creat(self):
        RBUT.building.creat(self)
        self.s.population += 11
        self.s.BaseCount += 1
        #print 'Increase BaseCount', self.s.BaseCount
Command_Center.__class__ = Command_Center_class


class TerranHousecls(RBUT.building):
    def __init__(self, origin):
        RBUT.building.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.BuildingPvd, origin.UnitPvd, origin.TechPvd, origin.BuildingReq, origin.UnitBusy, origin.UnitSpend, origin.UpgradeFrom)
        self.name = origin.name
        self.buildingReq = []
    def creat(self):
        self.s.population += 8
        RBUT.building.creat(self)
Supply_Depot = TerranHousecls(Supply_Depot)

class Orbital(Orbital_Command.__class__):
    __metaclass__ = Magical 
    #def energy():
        #'''A property class to override the operation over self.number.'''
        #def fget(self):
            #return 50
        #def fset(self, value):
            #print 'Why change this?', value
        #return locals()
    #energy = property(**energy())
    def __init__(self, origin):
        RBUT.building.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.BuildingPvd, origin.UnitPvd, origin.TechPvd, origin.BuildingReq, Command_Center, origin.UnitSpend, origin.UpgradeFrom)
        self.name = origin.name
        self.health = 1500
        self.shield = 0
        self.energy = 50
        self.stats = [1500, 0, 50]
        self.UnitBusy = Command_Center
    def make(self):
        if Orbital_Command.number + len(Orbital_Command.threadqueue) + Planetary_Fortress.number + len(Planetary_Fortress.threadqueue) >= Command_Center.number:return False
        if self.s.mineral >= self.MineReq and self.s.gas >= self.GasReq:pass
        else:return False
        if len(self.BuildingReq) > 0:
            if any([b.number == 0 for b in self.BuildingReq]):return False
        if self.UnitBusy:
            if self.UnitBusy.number == 0:return False
            if self.UnitBusy.occupied >= self.UnitBusy.number:return False
            self.UnitBusy.occupied += 1
            #print '***', self.UnitBusy, self.UnitBusy.number, self.UnitBusy.occupied
            return RBUT.things.build(self)
        #elif self.UpgradeFrom:
            #if self.UpgradeFrom.number == 0:return False
            #if self.UpgradeFrom.occupied == self.UpgradeFrom.number:return False
            #self.UpgradeFrom.occupied += 1
            #return things.build(self)
        #else:
            #return things.build(self)
Orbital_Command = Orbital(Orbital_Command)
#print Orbital_Command, Orbital_Command.stats, Orbital_Command.energy

#def useenergy(target, energy):
    #target.energy -= energy

class Mule_class(MULE.__class__):
    def __init__(self, origin):
        RBUT.unit.__init__(self, origin.MineReq, origin.GasReq, origin.TimeReq, origin.PopReq, origin.UnitReq, origin.NuReq,  BuildingBusy=origin.BuildingBusy, UpgradeFrom=origin.UpgradeFrom)
        self.name = 'MULE'
        self.BuildingReq = [Orbital_Command]
        self.history = 0
    def make(self):
        if Orbital_Command.number == 0:
            #print "MULE failed because of no Orbital"
            return False
        if all([OC[2] < 50 for OC in Orbital_Command.List]) :
            #print "MULE failed because Orbital does not have enough energy"
            #print Orbital_Command.List, Orbital_Command.stats
            return False
        for QC in Orbital_Command.List:
            if QC[2] >= 50:
                QC[2] += -50
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
MULE = Mule_class(MULE)
#MULE.Func = lambda self:useenergy(Orbital_Command, 50)

#Extra_Supplies = Mule_class(Supply_Depot)
class Extra_Supplies_class(MULE.__class__):
    def __init__(self, origin):
        RBUT.unit.__init__(self, 0, 0, 0, 0, origin.UnitReq, origin.NuReq,  BuildingBusy=origin.BuildingBusy, UpgradeFrom=origin.UpgradeFrom)
        self.name = 'Extra_Supplies'
        self.BuildingReq = [Orbital_Command]
    def make(self):
        if Supply_Depot.number - Extra_Supplies.number <= 0:
            #print 'Not enough Supply_Depot s!!!', Supply_Depot.number , Extra_Supplies.number 
            return False
        else:
            return MULE.__class__.make(self)
    def creat(self):
        #self.number += -1
        i = self.threadqueue.popleft()
        #if self.s.verbose:
            #print '%.1f s: %s %i broken' % (self.s.time, self.name, len(self.List))
    def build(self):
        t = self.s.time + self.TimeReq
        i = len(self.List)+len(self.threadqueue)
        heappush(self.s.queue, [t, [self,i]])
        self.threadqueue.append(i)
        self.number += 1
        self.s.population += 8 #extra supply
        self.s.log.append([self, self.s.mineral, self.s.time, self.TimeReq])
        if self.s.verbose:
            print '%dm%2.0fs: call down %s %i (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, len(self.List), self.s.PopOcupied, self.s.population)

        #return True
Extra_Supplies = Extra_Supplies_class(MULE)
#Extra_Supplies.Func = lambda self:useenergy(Orbital_Command, 50)
class Swaps(RBUT.things):
    def __init__(self, fromBuilding, toBuilding, addontype):
        self.addon = addontype
        self.name = 'Swap_'+  fromBuilding.name +'_'+ toBuilding.name +'_'+ addontype 
        self.MineReq = 0
        self.GasReq = 0
        self.TimeReq = 5
        self.fromBuilding = fromBuilding
        self.toBuilding = toBuilding
        self.fromaddon = globals()[fromBuilding.name+'_'+addontype]
        self.toaddon = globals()[toBuilding.name+'_'+addontype]
        self.BuildingReq = [self.fromaddon, toBuilding]
        self.threadqueue = deque([])
    def make(self):
        if self.fromaddon.number <= 0:return False
        if any([b.number - b.occupied <= 0 for b in [self.fromBuilding, self.toBuilding]]): return False 
        return self.build()
    def build(self, action=None, *args, **kwds):
        freeTechLab = [i for i in range(len(self.fromBuilding.List)) if len(self.fromBuilding.List[i]) >= 4 and self.fromBuilding.List[i][3] == 'f']
        if self.addon == 'Tech_Lab':
            if len(freeTechLab) <= 0:
                return False
            else:
                i = len(freeTechLab)
                j = freeTechLab[-1]
                self.fromBuilding.List[j] = self.fromBuilding.List[j][:3]
        elif self.addon == 'Reactor':
            NoOfFreeReactor = int((self.fromBuilding.number - self.fromBuilding.occupied - len(freeTechLab))/2)
            if NoOfFreeReactor <= 0:
                return False
            else:
                i = len(self.fromBuilding.List)
                self.fromBuilding.number += -1
        self.fromaddon.number += -1
        self.fromBuilding.occupied += 1
        self.toBuilding.occupied += 1
        t = self.s.time + self.TimeReq
        heappush(self.s.queue, [t, [self,i]])
        self.threadqueue.append(i)
        #if not self.Func == None:self.Func()#running the custumised function
        self.s.log.append([self, self.s.mineral, self.s.time, self.TimeReq])
        if self.s.verbose:
            print '%dm%2.0fs: Swapping %s (%d/%d)' % (int(self.s.time / 60), self.s.time % 60,  self.name, self.s.PopOcupied, self.s.population)
        return True
    def creat(self):
        i = self.threadqueue.popleft()
        self.fromBuilding.occupied += -1
        self.toBuilding.occupied += -1
        self.toaddon.number += 1
        if self.addon == 'Tech_Lab':
            for st in self.toBuilding.List:
                if len(st) < 4:
                    st.append('f')
                    break
        elif self.addon == 'Reactor':
            self.toBuilding.number += 1
        if self.s.verbose:
            print '%dm%2.0fs: Swapped %s (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, self.s.PopOcupied, self.s.population)

Swap_Barracks_Factory_Tech_Lab = Swaps(Barracks, Factory, 'Tech_Lab')
Swap_Barracks_Starport_Tech_Lab = Swaps(Barracks, Starport, 'Tech_Lab')
Swap_Factory_Starport_Tech_Lab = Swaps(Factory, Starport, 'Tech_Lab')
Swap_Starport_Factory_Tech_Lab = Swaps(Starport, Factory, 'Tech_Lab')
Swap_Barracks_Factory_Reactor = Swaps(Barracks, Factory, 'Reactor')
Swap_Barracks_Starport_Reactor = Swaps(Barracks, Starport, 'Reactor')
Swap_Factory_Starport_Reactor = Swaps(Factory, Starport, 'Reactor')
Swap_Starport_Factory_Reactor = Swaps(Starport, Factory, 'Reactor')

### From here after, general settings.

Command_Center.BuildingPvd = [Engineering_Bay]
Supply_Depot.BuildingPvd = [Barracks]
Barracks.BuildingPvd = [Orbital_Command, Bunker, Factory, Ghost_Academy, Reactor, Tech_Lab]
Engineering_Bay.BuildingPvd = [Planetary_Fortress, Sensor_Tower, Missile_Turret]
Factory.BuildingPvd = [Starport, Armory]
Starport.BuildingPvd = [Fusion_Core]

Command_Center.UnitPvd = [SCV]
Barracks.UnitPvd = [Marine]
Barracks_Tech_Lab.UnitPvd = [Marauder, Reaper, Ghost]
Ghost.BuildingReq.append(Ghost_Academy)
Orbital_Command.UnitPvd = [MULE, Extra_Supplies]
Factory.UnitPvd = [Hellion]
Factory_Tech_Lab.UnitPvd = [Siege_Tank, Thor]
Starport.UnitPvd = [Viking, Medivac, ]
Starport_Tech_Lab.UnitPvd = [Banshee, Raven, Battlecruiser]
Battlecruiser.BuildingBusy = Starport
Battlecruiser.BuildingReq.append(Fusion_Core)
Thor.BuildingBusy = Factory
Thor.BuildingReq.append(Armory)




allbuildings = [
Command_Center,
Supply_Depot,
Refinery,
Barracks,
Orbital_Command,
Planetary_Fortress,
Engineering_Bay,
Bunker,
Missile_Turret,
Sensor_Tower,
Factory,
Ghost_Academy,
Armory,
Starport,
Fusion_Core,
Tech_Lab,
Reactor,
]
allunits = [
SCV,
MULE,
Marine,
Marauder,
Reaper,
Ghost,
Hellion,
Siege_Tank,
Thor,
Viking,
Medivac,
Raven,
Banshee,
Battlecruiser,
AutoTurret,
Point_Defense_Drone,
Extra_Supplies,
]
alltechs = [
Terran_Infantry_Weapons_1,
Terran_Infantry_Weapons_2,
Terran_Infantry_Weapons_3, 
Terran_Infantry_Armor_1, 
Terran_Infantry_Armor_2,
Terran_Infantry_Armor_3,
HiSec_Auto_Tracking,
Neosteel_Frame,
Terran_Building_Armor, 
Stimpack ,
Combat_Shield ,
Nitro_Packs ,
Infernal_Pre_igniter,
Corvid_Reactor,
Caduceus_Reactor,
Durable_Materials,
Cloaking_Field,
Seeker_Missile,
Concussive_Shells,
Strike_Cannons,
Moebius_Reactor,
Personal_Cloaking,
Nuke,
Behemoth_Reactor,
Weapon_Refit,
Terran_Vehicle_Weapons_1,
Terran_Vehicle_Weapons_2, 
Terran_Vehicle_Weapons_3, 
Terran_Vehicle_Plating_1, 
Terran_Vehicle_Plating_2, 
Terran_Vehicle_Plating_3, 
Terran_Ship_Weapons_1, 
Terran_Ship_Weapons_2, 
Terran_Ship_Weapons_3, 
Terran_Ship_Plating_1, 
Terran_Ship_Plating_2, 
Terran_Ship_Plating_3, 
        ]
        
for building in allbuildings:
    building.UnitBusy = SCV



for b in [Barracks_Tech_Lab, Factory_Tech_Lab, Starport_Tech_Lab, Barracks_Reactor, Factory_Reactor, Starport_Reactor]:
    if b.name == 'Tech_Lab' or b.name == 'Reactor': 
        b.name = '%s_%s' % (b.attachto.name, b.name)
    allbuildings.append(b)

for b in [Barracks, Factory, Starport]:
    s = set(b.BuildingPvd)
    try:
        s.remove(Tech_Lab)
        s.remove(Reactor)
    except:pass
    s.add(locals()[b.name+'_Tech_Lab'])
    s.add(locals()[b.name+'_Reactor'])
    b.BuildingPvd = list(s)



for building in allbuildings:
    for sons in building.BuildingPvd:
        sons.BuildingReq.append(building)
    for unit in building.UnitPvd:
        unit.BuildingReq.append(building)

for bds in allbuildings:
    if bds.GasReq > 0:
        bds.BuildingReq.append(Refinery)
for uts in allunits:
    if uts.GasReq > 0:
        uts.BuildingReq.append(Refinery)
    if not uts.BuildingBusy == None:
        uts.BuildingReq.append(uts.BuildingBusy)
for tks in alltechs:
    if tks.GasReq > 0:
        tks.BuildingReq.append(Refinery)

class TechLabUnits(RBUT.unit):
    def HasTechLab(self):
        #print self.name, self.BuildingBusy.name
        freeTechLab = [st for st in self.BuildingBusy.List if len(st) >= 4 and st[3]=='f']
        #print 'HasTechLab:', freeTechLab
        if len(freeTechLab) >0 :
            freeTechLab[0][3] = 'o'
            return True
        else:
            return False
    def FreeTechLab(self):
        #print self.name, self.BuildingBusy.name
        OccupiedTechLab = [st for st in self.BuildingBusy.List if len(st) >= 4 and st[3]=='o']
        #print 'OccupiedTechLab:', OccupiedTechLab
        if len(OccupiedTechLab) >0 :
            OccupiedTechLab[0][3] = 'f'
            return True
        else:
            return False
    def build(self):
        if self.HasTechLab():
            return RBUT.unit.build(self)
        else:
            return False
    def creat(self):
        if self.FreeTechLab():
            return RBUT.unit.creat(self)
        else:
            return False


for ut in [Marauder, Reaper, Ghost, Siege_Tank, Thor, Banshee, Raven ]:
    ut.__class__ = TechLabUnits




class terran(RBUT.race):
    def __init__(self, timestep=1.5):
        RBUT.race.__init__(self, 'terran', timestep)
        self.allbuildings = allbuildings
        self.allunits = allunits
        self.alltechs  = alltechs
        self.startbuildings = [Command_Center]
        self.startunits = [(SCV, 6)]
        self.Miner = SCV 
        self.geyser = Refinery
        self.House = Supply_Depot 
        self.InitialPopulation = 11
        self.population = self.InitialPopulation
        self.restart()
    def restart(self):
        RBUT.race.restart(self)
        MULE.history = 0
    def CalculateResourse(self, time):
        lapse = time - self.time
        self.mineral += self.mineralrate()*lapse + (MULE.number-MULE.occupied)*10./3*lapse
        self.gas += self.GasMiner*0.555555555555555*lapse #112/3/60
        for unit in self.MagicalList:
            for individual in unit.List:
                individual[2] = min(200, individual[2] + 50./90 * lapse)

import copy ,sys
from fileio import *
from heapq import *
from collections import deque


class things(object):
    def __init__(self, MineReq, GasReq, TimeReq, Func=None):
        self.name = ''
        self.MineReq = MineReq
        self.GasReq = GasReq
        self.TimeReq = TimeReq
        self.BuildingReq = []
        self.Func = Func
        self.List = []
        self.health = 50
        self.shield = 0
        self.energy = 50
        self.stats = [int(self.health), int(self.shield), int(self.energy)]
        self.threadqueue = deque([])
        self.occupied = 0
        self.s = None
    def number():
        '''A property class to override the operation over self.number.'''
        def fget(self):
            return len(self.List)
        def fset(self, value):
            l = len(self.List)
            i = value - l
            if l == 0 and i > 0:
                if issubclass(self.__class__, building):
                    self.s.buidlings.append(self)
                elif issubclass(self.__class__, unit):
                    self.s.units.append(self)
            if i > 0:
                while i > 0:
                    self.List.append(copy.deepcopy(self.stats))
                    i += -1
            elif i < 0:
                while i < 0:
                    self.List = self.List[:-1]
                    i += 1
        return locals()
    number = property(**number())
    def __str__(self):
        return ' '.join(self.name.split('_'))
    def creat(self):
        self.number += 1
        i = self.threadqueue.popleft()
        if self.s.verbose:
            if self in [Barracks, Factory, Starport]:
                print '%dm%2.0fs: %s %i created (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, len(self.List) - globals()[self.name+'_Reactor'].number, self.s.PopOcupied, self.s.population)
            else:
                print '%dm%2.0fs: %s %i created (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, len(self.List), self.s.PopOcupied, self.s.population)
    def build(self, action=None, *args, **kwds):
        self.s.mineral = self.s.mineral - self.MineReq
        self.s.gas = self.s.gas - self.GasReq
        t = self.s.time + self.TimeReq
        if not self.Func == None:self.Func()#running the custumised function
        i = len(self.List)+len(self.threadqueue)
        heappush(self.s.queue, [t, [self,i]])
        self.threadqueue.append(i)
        self.s.log.append([self, self.s.mineral, self.s.time, self.TimeReq])
        if self.s.verbose:
            if self.__dict__.has_key('PopReq') and self.PopReq > 0:
                print '%dm%2.0fs: creating %s %i (%d/%d)' % (int(self.s.time / 60), self.s.time % 60,  self.name, len(self.List)+len(self.threadqueue), self.s.PopOcupied + self.PopReq, self.s.population)
            else:
                if self in [Barracks, Factory, Starport]:
                    print '%dm%2.0fs: creating %s %i (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, len(self.List)+len(self.threadqueue)-globals()[self.name+'_Reactor'].number, self.s.PopOcupied, self.s.population)
                else:
                    print '%dm%2.0fs: creating %s %i (%d/%d)' % (int(self.s.time / 60), self.s.time % 60, self.name, len(self.List)+len(self.threadqueue), self.s.PopOcupied, self.s.population)
        return True
    def cancel(self):
        self.s.mineral += 0.75 * self.MineReq
        self.s.gas += 0.75 * self.GasReq
        i = self.threadqueue.popleft()
        for j in range(len(self.s.queue)):
            if self.s.queue[j][1][0] == self:
                if self.s.queue[j][1][1] == i: 
                    t = self.s.queue[j][0]
                    self.s.queue[j][0] = -1
                    heapify(self.s.queue)
                    heappop(self.s.queue)
                    for log in self.s.log:
                        if log[0] == self and log[2]+log[3] == t:
                            log[3] = self.s.time - log[2]
                    if self.s.verbose:
                        print '%.1f s: %s cancelled (%d/%d)' % (self.s.time, self.name, self.s.PopOcupied, self.s.population)
                    return True

class building(things):
    def __init__(self, MineReq, GasReq, TimeReq, BuildingPvd=(), UnitPvd=(), TechPvd=(), BuildingReq=None, UnitBusy=None, UnitSpend=None, UpgradeFrom=None):
        things.__init__(self, MineReq, GasReq, TimeReq)
        self.BuildingPvd=BuildingPvd
        self.UnitPvd=UnitPvd
        if BuildingReq == None:
            self.BuildingReq = []
        else:
            self.BuildingReq = BuildingReq
        self.UnitSpend = UnitSpend
        self.UnitBusy = UnitBusy
        self.UpgradeFrom = UpgradeFrom
        if TechPvd == ():
            self.TechPvd = []
        else:
            self.TechPvd = TechPvd
    def creat(self):
        if self.number == 0:
            self.s.BuildingList.append(self)
        things.creat(self)
        if self.UnitBusy:
            self.UnitBusy.occupied += -1
        if self.UpgradeFrom:
            self.UpgradeFrom.occupied += -1
            self.UpgradeFrom.number += -1
    def make(self):
        if self.s.mineral >= self.MineReq and self.s.gas >= self.GasReq:pass
        else:return False
        if not len(self.BuildingReq) == 0 or self.BuildingReq == None:
            if any([b.number == 0 for b in self.BuildingReq]):return False
        if self.UnitSpend:
            if self.UnitSpend.number - self.UnitSpend.occupied > 0:
                self.UnitSpend.number += -1
                self.s.PopOcupied += -1* self.UnitSpend.PopReq
                return things.build(self)
            else:return False
        if self.UnitBusy:
            if self.UnitBusy.number == 0:return False
            if self.UnitBusy.occupied >= self.UnitBusy.number:return False
            self.UnitBusy.occupied += 1
            return things.build(self)
        if self.UpgradeFrom:
            if self.UpgradeFrom.number == 0:return False
            if self.UpgradeFrom.occupied >= self.UpgradeFrom.number:return False
            self.UpgradeFrom.occupied += 1
            return things.build(self)
        else:
            return things.build(self)
    def build(self):
        return self.make()
    def cancel(self):
        if self.UnitSpend:
            self.UnitSpend.number += 1
            self.s.PopOcupied += self.UnitSpend.PopReq
        elif self.UnitBusy:
            self.UnitBusy.number += 1
        return things.cancel(self)

class unit(things):
    def __init__(self, MineReq, GasReq, TimeReq, PopReq, UnitReq=None, NuReq=0, damage=0, cooldown=0, speed=0, BuildingReq=None, BuildingBusy=None, UpgradeFrom=None):
        things.__init__(self, MineReq, GasReq, TimeReq)
        self.PopReq = PopReq
        self.UnitReq = UnitReq
        self.NuReq =NuReq
        if BuildingReq == None:
            self.BuildingReq = []
        else:
            self.BuildingReq = BuildingReq
        if BuildingBusy == 'None':
            BuildingBusy = None
        self.BuildingBusy = BuildingBusy
        self.UpgradeFrom = UpgradeFrom
    def creat(self):
        if self.number == 0:
            self.s.UnitList.append(self)
        things.creat(self)
        if self.BuildingBusy:self.BuildingBusy.occupied += -1
        if self.UpgradeFrom:
            self.UpgradeFrom.occupied += -1
            self.UpgradeFrom.number += -1

    def make(self):
        if self.s.mineral >= self.MineReq and self.s.gas >= self.GasReq:pass
        else:return False
        if not len(self.BuildingReq) == 0 or self.BuildingReq == None:
            if any([b.number == 0 for b in self.BuildingReq]): return False 
        if self.s.population - self.s.PopOcupied < self.PopReq and not self.PopReq == 0: return False
        if self.UnitReq:
            if self.UnitReq.number == 0:return False
            self.s.PopOcupied += self.PopReq
            Flag = things.build(self)
            self.UnitReq.number = self.UnitReq.number - self.NuReq
            self.s.PopOcupied += (-1 * self.UnitReq.PopReq)
            return Flag
        elif self.UpgradeFrom:
            if self.UpgradeFrom.number == 0:return False
            if self.UpgradeFrom.occupied == self.UpgradeFrom.number:return False
        else:
            if self.BuildingBusy:
                if self.BuildingBusy.occupied >= self.BuildingBusy.number:
                    return False
                else:
                    self.BuildingBusy.occupied += 1
            #return things.build(self)
            if self.build():
                self.s.PopOcupied += self.PopReq
                return True
            else:
                return False
    def transform(self, NewUnit):
        return NewUnit.build()
    def produce(self):
        return self.make()
    def cancel(self):
        things.cancel(self)
        self.s.PopOcupied = self.s.PopOcupied - self.PopReq

class tech(things):
    def __init__(self, MineReq, GasReq, TimeReq, BuildingBusy, BuildingReq):
        self.researched = False
        things.__init__(self, MineReq, GasReq, TimeReq)
        self.BuildingBusy = BuildingBusy
        self.BuildingReq = list(set(BuildingReq)|set([BuildingBusy]))
        self.TechReq = []
    def creat(self):
        things.creat(self)
        self.researched = True
    def make(self):
        if self.s.mineral >= self.MineReq and self.s.gas >= self.GasReq:pass
        else:return False
        if any([b.number == 0 for b in self.BuildingReq]):return False
        if self.TechReq:
            if not self.TechReq.researched: return False
        if self.BuildingBusy.occupied < self.BuildingBusy.number:
            self.BuildingBusy.occupied += 1
        else:
            return False
        return self.build()
    def research(self):
        self.make()


#def MinerCount():
    #""" Use this descriptor to override the Drone.number's access, so that I can keep track on the number of Drones and calculate mining right""" 
    #def fget(self):
        #return len(self.List)
    #def fset(self, value):
        #i = value - len(self.List)
        #self.s.MineralMiner += i
        #if i > 0:
            #while i > 0:
                #self.List.append(self.stats)
                #i += -1
        #elif i < 0:
            #while i < 0:
                #self.List = self.List[:-1]
                #i += 1
    #return locals()



class race(object):
    def __init__(self, name, timeout):
        self.name = name
        self.time = 0
        self.timeout = timeout
        #self.timestep = timestep 
        self.TechTree = {}
        self.BuildingList = {}
        self.UnitList = {}
        self.allbuidlings = ()
        self.allunits = ()
        self.alltechs = ()
        self.startbuidlings = ()
        self.startunits = ()
        self.buidlings = []
        self.units = []
        self.mineral = 50
        self.gas = 0
        self.InitialPopulation = 10
        self.population = self.InitialPopulation
        self.Miner = []
        self.geyser = []
        #self.MineralMiner = 6
        self.GasMiner = 0
        self.PopOcupied = 6
        self.MagicalList = set([])
        self.log = []
        self.BaseCount = 1
        self.queue = []
        self.House = []
        self.verbose = True
    #def Mining(self):
        #class newcls(self.Miner.__class__):
            #number = property(**MinerCount())
        #self.Miner.__class__ = newcls
        #class AddMineral():
            #def __init__(self,s):
                #self.s = s
                #self.interval = 7.7 #s
                #self.go = True
            #def creat(self):
                #if self.s.MineralMiner > 24*self.s.BaseCount:
                    #MinerCount = 24
                #else:MinerCount = self.s.MineralMiner
                #self.s.mineral += (5 * MinerCount)
                #if self.go:
                    #self.make()
            #def make(self):
                #t = self.s.time + self.interval
                #i = 'm'
                #heappush(self.s.queue, [t, [self,i]])
        #class AddGas():
            #def __init__(self,s):
                #self.s = s
                #self.interval =  6.6 #s
                #self.go = True
            #def creat(self):
                #GaserCount = self.s.GasMiner
                #if GaserCount > self.s.geyser.number * 3 and self.s.geyser.number <= self.s.BaseCount * 2: 
                    #GaserCount = self.s.geyser.number * 3
                #elif  GaserCount > self.s.BaseCount * 6:
                    #GaserCount = self.s.BaseCount * 6
                #self.s.gas += (4 * GaserCount)
                #if self.go:
                    #self.make()
            #def make(self):
                #t = self.s.time + self.interval
                #i = 'g'
                #heappush(self.s.queue, [t, [self,i]])
        #self.m = AddMineral(self)
        #self.g = AddGas(self)
    #def StopMining(self):
        #self.m.go = False
        #self.g.go = False
    def restart(self):
        self.buildings = []
        self.units = []
        for BD in self.allbuildings:
            BD.number = 0
            BD.occupied = 0
            BD.threadqueue = deque([])
            BD.s = self
        for UT in self.allunits:
            UT.number = 0
            UT.occupied = 0
            UT.threadqueue = deque([])
            UT.s = self
        for TK in self.alltechs:
            TK.researched = False
            TK.threadqueue = deque([])
            TK.s = self
            TK.number = 0
        for BD in self.startbuildings:
            BD.number = 1
            BD.List = [copy.deepcopy(BD.stats)]
        for UT in self.startunits:
            UT[0].number = UT[1]
        self.BuildingList = []
        for BD in self.startbuidlings:
            self.BuildingList.append(BD)
        self.UnitList = []
        for UT in self.startunits:
            self.UnitList.append(UT)
            for i in range(UT[1]):
                #UT[0].List.append(copy.deepcopy(UT[0].stats))
                UT[0].number = UT[1]
        self.mineral = 50
        self.gas = 0
        self.population = self.InitialPopulation
        self.PopOcupied = 6
        #self.MineralMiner = 6
        #self.Miner.number = 6
        self.GasMiner = 0
        self.geyser.__class__ = GeyserCls
        self.time = 0
        self.log = []
        self.BaseCount = 1
        self.queue = []
        self.MagicalList = set([])
        """Set up a dynamic simulating loop"""
        self.time = 0
        #self.timeout = timeout
        Dummy = things(0,0,0)
        Dummy.threadqueue.append(-1)
        Dummy.s=self
        Dummy.name = 'End of simulation.'
        heappush(self.queue, (self.timeout, (Dummy, 1000)))
    def make(self, sth):
        if self.mineral >= sth.MineReq and self.gas >= sth.GasReq:
            return sth.make()
        else:
            return False
    def run(self):pass
    def mineralrate(self):
        def rate(N):
            if N == 0:
                return 0.01
            elif N < 17:
                return 42./60.* N
            elif N < 21:
                return (380.+19.*N)/60.
            elif N < 25:
                return (480. + 14.*N)/60.
            elif N >= 25:
                return (830.)/60

        M = self.Miner.number - self.Miner.occupied - self.GasMiner
        B = self.BaseCount
        if B == 1:
            return rate(M)
        else:
            N = M /B
            E = M % B
            return rate(N+1)*E + rate(N)*(B-E)

    def CalculateResourse(self, time):
        lapse = time - self.time
        self.mineral += self.mineralrate()*lapse
        self.gas += min(self.GasMiner,self.BaseCount*6)*0.555555555555555*lapse #112/3/60
        for unit in self.MagicalList:
            for individual in unit.List:
                individual[2] = min(200, individual[2] + 50./90 * lapse)

    def mainloop(self, run, *args, **kwds):
        """ The Mainloop of the simulation"""
        #self.m.make()
        self.time = 0
        Dummy = things(0,0,0)
        Dummy.threadqueue.append(-1)
        Dummy.s=self
        Dummy.name = 'End of simulation.'
        heappush(self.queue, (self.timeout, (Dummy, 1000)))
        #count = 0
        while self.time < self.timeout:
            run(*args, **kwds)
            (now, (item, i)) = heappop(self.queue)
            self.CalculateResourse(now)
            self.time = now
            item.creat()
            #count += 1
        #print 'Number of loops' , count
    def prepareflow(self):
        """Set up a dynamic simulating loop"""
        self.time = 0
        #self.timeout = timeout
        Dummy = things(0,0,0)
        Dummy.threadqueue.append(-1)
        Dummy.s=self
        Dummy.name = 'End of simulation.'
        heappush(self.queue, (self.timeout, (Dummy, 1000)))
        #while true:
            #(now, (item, i)) = heappop(self.queue)
            #if now >= timeout: break
    def evaluate(self, Q):
        while True:
            Q.make()
            (now, (item, i)) = heappop(self.queue)
            if len(self.queue) == 0:
                endgame = False # did not reach the end time
                heappush(self.queue, (now, (item, i)))
                break
            self.CalculateResourse(now)
            self.time = now
            item.creat()
            if now > self.timeout:
                endgame = True # reach the end time
                break
        #print Q.done
        if len(Q.queue) == 0:
            return endgame, len(Q.queue), (-1, DummyItem(self, name='END'))
        else:
            return endgame, len(Q.queue), heappop(Q.queue)

        






class Magical(type):
    def __new__(mcl, name, base, dict):
        cls = super(Magical, mcl).__new__(mcl, name, base, dict)
        _creat = cls.creat
        def creat(self):
            if self.number == 0:
                self.s.MagicalList.add(self)
            _creat(self)
        cls.creat = creat
        return cls

from Control import *
from Control import _sendtogeyser

class GeyserCls(building):
    buildingReq = []
    def creat(self):
        building.creat(self)
        #self.s.g.make()
        if self.s.Miner.number - self.s.Miner.occupied < 3:
            _sendtogeyser(self.s, self.s.Miner.number - self.s.Miner.occupied)
        else:
            _sendtogeyser(self.s,3)

names = readcol('buildings.dat', 0)
mineral = readcol('buildings.dat', 1)
gas = readcol('buildings.dat', 2)
buildtime = readcol('buildings.dat', 3)

for i in range(len(names)):
    exec('%s = building(mineral[i], gas[i], buildtime[i])' % names[i])
    obj = locals()[names[i]]
    globals().update({names[i]:obj})
    exec('%s.name = "%s"' % (names[i], names[i]) )

#Barracks_Tech_Lab = building(50, 25, 25, BuildingReq=[Barracks], UpgradeFrom=Barracks)
#Factory_Tech_Lab = building(50, 25, 25, BuildingReq=[Factory], UpgradeFrom=Factory )
#Starport_Tech_Lab = building(50, 25, 25, BuildingReq=[Starport], UpgradeFrom=Starport)

class addon(building):
    def __init__(self, *a, **k):
        building.__init__(self, *a, **k)
        self.attachto = None
    def make(self):
        if self.s.mineral >= self.MineReq and self.s.gas >= self.GasReq:pass
        else:
            return False
        if len(self.BuildingReq) > 0:
            if any([ b.number ==0 for b in self.BuildingReq]):
                return False
        if self.UnitSpend:
            if self.UnitSpend.number - self.UnitSpend.occupied > 0:
                self.UnitSpend.number += -1
                self.s.PopOcupied += -1* self.UnitSpend.PopReq
                return things.build(self)
            else:return False
        if self.attachto.number <= 0 or self.attachto.number - self.attachto.occupied == 0:
            return False
        alongBD = [st for st in self.attachto.List if len(st) == 3]
        #print self.attachto.List
        #print 'alongBD:', alongBD, 2*globals()[self.attachto.name+'_Reactor'].number
        if len(alongBD) - 2*globals()[self.attachto.name+'_Reactor'].number <= 0 : return False
        #if not self.name.find('Tech_Lab') == -1:
        #if not self.name.find('Reactor') == -1:
            
        building.make(self)
        return True
    def creat(self):
        building.creat(self)
        self.function(self)
    def swap(self, other):
        if other.number > 0 and other.number - other.occupied > 0:
            if self.defunction(self):
                self.number += -1
                globals()['_'.join([other.name, self.name])].number +=1
                self.attachto = other
                self.function(self)
                return True
            else:
                return False
        else:
            return False
    def function(self):pass
    def defunction(self):pass
Reactor.__class__ = addon
Tech_Lab.__class__ = addon

def f_reactor(self):
    self.attachto.number += 1
    return True
Reactor.function = f_reactor
def df_reactor(self):
    FreeTechLab = len([st for st in self.attachto.List if len(st) >= 4 and st[3] == 'f'])
    NoOfFreeReactor = int((self.attachto.number - self.attachto.occupied - FreeTechLab)/2)
    if NoOfFreeReactor == 0:
        return False
    else:
        self.attachto.number += -1
        return True
Reactor.defunction = df_reactor
def f_Tech_Lab(self):
    for st in self.attachto.List:
        if len(st) < 4:
            st.append('f')
            return True
    return False
    #[st for st in self.attachto.List if len(st) < 4][0].append('f')
Tech_Lab.function = f_Tech_Lab
def df_Tech_Lab(self):
    freeTechLab = [st for st in self.attachto.List if len(st) >= 4 and st[3] == 'f']
    if len(freeTechLab) > 0:
        freeTechLab[-1].pop('f')
        return True
    else:
        return False
Tech_Lab.defunction = df_Tech_Lab
    
#Reactor.BuildingBusy
from copy import deepcopy
Tech_Lab.UnitBusy = None
#Barracks_Tech_Lab.UpgradeFrom = Barracks
#Factory_Tech_Lab.UpgradeFrom = Factory
#Starport_Tech_Lab.UpgradeFrom = Starport 
Barracks_Tech_Lab = deepcopy(Tech_Lab)
Factory_Tech_Lab = deepcopy(Tech_Lab)
Starport_Tech_Lab = deepcopy(Tech_Lab)
Barracks_Reactor = deepcopy(Reactor)
Factory_Reactor = deepcopy(Reactor)
Starport_Reactor = deepcopy(Reactor)
#Barracks_Reactor.UpgradeFrom = Barracks
#Factory_Reactor.UpgradeFrom = Factory
#Starport_Reactor.UpgradeFrom = Starport 
#Orbital_Command.UpgradeFrom = Command_Center
Orbital_Command.UnitBusy = Command_Center
Barracks_Tech_Lab.UnitBusy = Barracks
Factory_Tech_Lab.UnitBusy = Factory
Starport_Tech_Lab.UnitBusy = Starport
Barracks_Reactor.UnitBusy = Barracks
Factory_Reactor.UnitBusy = Factory
Starport_Reactor.UnitBusy = Starport
Barracks_Tech_Lab.attachto = Barracks
Factory_Tech_Lab.attachto = Factory
Starport_Tech_Lab.attachto = Starport
Barracks_Reactor.attachto = Barracks
Factory_Reactor.attachto = Factory
Starport_Reactor.attachto = Starport
Planetary_Fortress.UpgradeFrom = Command_Center
#Barracks_Tech_Lab.name = 'Tech Lab'
#Barracks_Reactor.name = 'Reactor'


names = readcol('units.dat', 0)
mineral = readcol('units.dat', 1)
gas = readcol('units.dat', 2)
buildtime = readcol('units.dat', 3)
popreq = readcol('units.dat', 4)
buildingbusy = readcol('units.dat', 5)


for i in range(len(names)):
    exec('%s = unit(mineral[i], gas[i], buildtime[i], popreq[i], BuildingBusy=%s)' % (names[i], buildingbusy[i]))
    obj = locals()[names[i]]
    globals().update({names[i]:obj})
    exec('%s.name = "%s"' % (names[i], names[i]) )

names = readcol('techs.dat', 0)
mineral = readcol('techs.dat', 1)
gas = readcol('techs.dat', 2)
taketime = readcol('techs.dat', 3)
buildingbusy = readcol('techs.dat', 4)
buildingreq = readcol('techs.dat', 5)


for i in range(len(names)):
    #try:
    exec('%s = tech(mineral[i], gas[i], taketime[i], %s, [%s] )' % (names[i], buildingbusy[i], buildingreq[i]) )
    #except:
        #print '%s = tech(mineral[i], gas[i], taketime[i], %s )' % (names[i],buildingreq[i])
    obj = locals()[names[i]]
    globals().update({names[i]:obj})
    exec('%s.name = "%s"' % (names[i], names[i]) )
for i in range(len(names)):
    exec('%s.TechPvd.append(%s)' % (buildingreq[i], names[i]) )

#from RBUT import *
from heapq import *

class Action(object):
    def __init__(self, Func, simulator, *args, **kwds):
        self.name = repr(Func)
        self.simulator = simulator
        self.done = False
        self.Func = Func
        self.args = args
        self.kwds = kwds
    def make(self):
        self.done = self.Func(self.simulator, *self.args, **self.kwds)
        return self.done
    def __str__(self):
        return self.name

def _sendtogeyser(s,N):
    if N > s.Miner.number - s.Miner.occupied: raise Error
    s.GasMiner += N
    return True

sendtogeyser = lambda simulator, N: Action(_sendtogeyser, simulator, N)

class DummyItem(object):
    def __init__(self, simulator, name='Dummy'):
        self.name=name
    def make(self):return True
    def creat(self):return True
    def __str__(self):return self.name
    def __repr__(self):return self.name+' <Control.Item>'


class Item(object):
    def __init__(self, obj, simulator, Flag = False):
        self.name = obj.name
        self.object = obj
        self.simulator = simulator
        self.object.s = simulator
        self.done = Flag
    def make(self):
        if not self.object.s:self.object.s = self.s
        self.done = self.object.make()
        #prediction mode
        if not self.done:
            if self.object.name in set(['MULE', 'Extra_Supplies']):
                if any([b.number == 0 for b in self.object.BuildingReq]):return self.done
                MostEnegetic = sorted([sts for sts in self.object.BuildingReq[0].List], key=lambda x:x[2])[-1][2]
                if MostEnegetic > 50: 
                    #print self.object.BuildingReq[0].List
                    #raise EnoughOfEnergy
                    return False
                t = (50. - MostEnegetic) * 90/50. + self.simulator.time + 0.01
                heappush(self.simulator.queue, [t, (DummyItem(self.simulator), -1)])
            import RBUT
            if issubclass(self.object.__class__, RBUT.things): 
                if not len(self.object.BuildingReq) == 0 and any([b.number == 0 for b in self.object.BuildingReq]):return self.done
                if self.object.MineReq > self.simulator.mineral:
                    t =(self.object.MineReq - self.simulator.mineral)/self.simulator.mineralrate() + self.simulator.time + 0.01
                    #except RuntimeWarning:
                        #print self.object.name, self.simulator.mineralrate(), self.simulator.Miner.number
                        #raise stophere
                    heappush(self.simulator.queue, [t,(DummyItem(self.simulator), -1)])
                elif not self.object.GasReq == 0 and self.object.GasReq > self.simulator.gas and not self.simulator.GasMiner == 0:
                    t = self.simulator.time + (self.object.GasReq > self.simulator.gas)/self.simulator.GasMiner/1.292222222 + 0.01
                    heappush(self.simulator.queue, [t, (DummyItem(self.simulator), -1)])

                
        return self.done
    def __str__(self):
        return self.name

class CancelItem(Item):
    def __init__(self, obj, simulator ):
        Item.__init__(self, obj, simulator)
        self.name = 'Cancel '+self.name
    def make(self):
        #try:
        if self.object.cancel():
            self.done = True
            return True
        #except:
        return False

class NumberItem(Item):
    def __init__(self, obj, simulator, Number):
        Item.__init__(self, obj, simulator)
        self.Number = Number
        self.s = simulator
    def make(self):
        if self.Number == 'IDF':
            def MakingHouse():
                for item in self.s.queue:
                    if item[1][0] == self.s.House:
                        return True
            if self.object.BuildingBusy and not self.object.BuildingBusy.number == 0 and not self.object.TimeReq == 0:
                N = int(self.s.House.TimeReq/self.object.TimeReq/self.object.BuildingBusy.number)+1
            else:
                N = int(self.s.House.TimeReq/self.object.TimeReq)+1
            if self.s.population - self.s.PopOcupied < N * self.object.PopReq and not MakingHouse():
                self.s.House.s=self.s
                self.s.House.make()
            else: 
                if not self.object.s:self.object.s = self.s
                while self.object.make():self.make()
            return False
        else:
            while not self.Number == 0:
                if Item.make(self): 
                    self.Number += -1
                    self.make()
                else:
                    return False
            self.done = True
            return self.done

class ConditionItem(Item):
    def __init__(self, obj, simulator, condition, *args, **kwds):
        Item.__init__(self, obj, simulator)
        self.condition = condition
        self.args = args
        self.kwds = kwds
    def make(self):
        if self.condition(*self.args, **self.kwds):
            if Item.make(self):
                self.done = True
                return True
            

        
class TimingItem(Item):
    def __init__(self, obj, simulator, moment):
        Item.__init__(self, obj, simulator)
        self.time = moment
    def make(self):
        if self.simulator.time > self.time: 
            if Item.make(self):
                self.done = True
        #else:
            #heappush(self.simulator.queue, (self.time, [self.object, 1]) )

class DelayItem(Item):
    def __init__(self, obj, simulator, wait):
        Item.__init__(self, obj, simulator)
        self.time = wait
    def make(self):
        heappush(self.simulator.queue, (self.simulator.time + self.time , [Item(self.object, self.simulator), 1]) )

class pipeline(object):
    def __init__(self, list):
        self.done = False
        self.queue = []
        for item in list:
            heappush(self.queue, item)
    def make(self):
        if self.queue:
            index, item = heappop(self.queue)
            item.make()
            if item.done:
                if len(self.queue) == 0:
                    pass
                else:
                    self.make()
            else:
                #while not self.make():pass
                heappush(self.queue, (index, item))
        else:
            self.done = True
        return self.done

class workflow(object):
    def __init__(self, list):
        self.done = False
        self.flow = list
    def make(self):
        return all([item.make() for item in self.flow])


class Combo(object):
    def __init__(self, list, name='Combo'):
        self.name = name
        self.done = False
        self.queue = []
        for item in list:
            heappush(self.queue, item)
    def make(self):
        while self.queue:
            index, item = heappop(self.queue)
            if not item.make():
                heappush(self.queue, (index, item))
                return False
        self.done = True
        return self.done

HavestGas = lambda simulator: NumberItem(simulator.geyser, simulator, 1)
StopHavestGas = lambda simulator: sendtogeyser(simulator, -3)


        





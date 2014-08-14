#from Traverse import fitness, Node
class PopulationAnomaly(BaseException):pass
class Anomaly(BaseException):pass


def alphabets(s):
    availables = [SCV, Supply_Depot, Refinery]
    NoGasUnit = [SCV, MULE, Marine, Hellion]
    NoGasBD = [Barracks, Orbital_Command, Engineering_Bay, Supply_Depot]
    HasRefinery = False
    if Refinery in s.buildings:HasRefinery = True
    TwoRefinery = False
    if len([r for r in s.buildings if r == Refinery]) >= 2:
        TwoRefinery = True
    for b in s.buildings:
        availables += [bd for bd in b.BuildingPvd if HasRefinery or bd in NoGasBD]
        availables += [ u for u in b.UnitPvd if HasRefinery or u in NoGasUnit]
    if TwoRefinery:
        availables = list(set(availables).remove(Refinery))
    return availables

from itertools import imap, count
from random import choice, shuffle

#default = set([SCV, Marine, Supply_Depot, Refinery, Barracks, Barracks_Reactor, Orbital_Command, MULE, Extra_Supplies, Factory, Factory_Reactor, Hellion])
default = set([SCV, Marine, Supply_Depot, Refinery, Barracks, Barracks_Tech_Lab, Orbital_Command, MULE, Extra_Supplies, Marauder])
#def avGene(genome, allowed = default):
class GeneSelector(object):
    def __init__(self):
        self.allowed = default
    def __call__(self, genome):
        allowed = self.allowed
        simulator = genome.simulator #only works with non-zero genome
        #allowed = set([SCV, Marine, Supply_Depot, Refinery, Barracks, Barracks_Reactor, Orbital_Command, MULE, Extra_Supplies, Factory, Factory_Reactor, Hellion])
        availables = set([SCV, Supply_Depot, Refinery])
        NoGasUnit = [SCV, MULE, Marine, Hellion]
        NoGasBD = [Barracks, Orbital_Command, Engineering_Bay, Supply_Depot]
        objlist = [g.object for g in genome]
        HasRefinery = False
        if Refinery in objlist:HasRefinery = True
        TwoRefinery = False
        if len([r for r in objlist if r == Refinery]) >= 2:
            TwoRefinery = True
        NoFreeBarracks = 0
        NoFreeFactories = 0
        NoFreeStarports = 0
        NoOfCC = 0
        NoOfOC = 0
        NoOfSD = 0
        NoOfES = 0
        NoOfSCV = 0
        for g in objlist:
            if g == Barracks:
                NoFreeBarracks += 1
            elif g == Barracks_Tech_Lab:
                NoFreeBarracks += -1
            elif g == Barracks_Reactor:
                NoFreeBarracks += -1
            if g == Factory:
                NoFreeFactories+= 1
            elif g == Factory_Tech_Lab:
                NoFreeFactories += -1
            elif g == Factory_Reactor:
                NoFreeFactories += -1
            if g == Starport:
                NoFreeStarports += 1
            elif g == Starport_Tech_Lab:
                NoFreeStarports += -1
            elif g == Starport_Reactor:
                NoFreeStarports += -1
            if g == Command_Center:NoOfCC += 1
            if g == Orbital_Command:NoOfOC += 1
            if g == Supply_Depot:NoOfSD += 1
            if g == Extra_Supplies:NoOfES += 1
            if g == SCV :NoOfSCV += 1
            try:
                availables |= set([bd for bd in g.BuildingPvd if HasRefinery or bd in NoGasBD])
                availables |= set([ u for u in g.UnitPvd if HasRefinery or u in NoGasUnits])
            except:pass
        #NoOfCC = len([cc for cc in objlist if cc == Command_Center])
        #NoOfOC = len([cc for cc in objlist if cc == Orbital_Command])
        #try:
        if NoFreeBarracks == 0:
            availables = availables - set([Barracks_Tech_Lab, Barracks_Reactor])
        if NoFreeFactories == 0:
            availables = availables - set([Factory_Tech_Lab, Factory_Reactor])
        if NoFreeStarports == 0:
            availables = availables - set([Starport_Tech_Lab, Starport_Reactor])
        #except:pass
        #NoOfSCV = len([scv for scv in objlist if scv == SCV])
        #if NoOfSCV < 2:
            #availables.remove(Supply_Depot)
        #else:
            #availables.add(Supply_Depot)
        if HasRefinery and NoOfSCV == 0:
            availables.remove(Refinery)
        if NoOfSCV > 0 and not TwoRefinery:
            availables.add(Refinery)
        if not len(genome) == 0:
            availables = set([it for it in availables & allowed if not issubclass(it.__class__, RBUT.unit) or it.PopReq <= genome.nodes[-1]['PopAvl']])
        else:
            #availables = [it for it in availables & allowed if not issubclass(it.__class__, RBUT.unit) or it.PopReq <= 6]
            availables = availables & allowed
        if TwoRefinery:
            availables.remove(Refinery)
        if NoOfOC > NoOfCC:
            availables = availables - set([Orbital_Command, Planetary_Fortress])
        if NoOfES >= NoOfSD and NoOfES > 0:
            availables = availables - set([Extra_Supplies])
        if Orbital_Command in objlist:
            availables = availables - set([Orbital_Command, Planetary_Fortress])
        return [Item(a, simulator) for a in availables]
#from math import mean
avGene = GeneSelector()

def Fitness(simulator):
    t = []
    m = []
    s = []
    b = []
    o = []
    M = []
    e = []
    for log in simulator.log:
        if log[0] == Marine:t.append(float(log[2])/simulator.timeout)
        if log[0] == Marauder:m.append(float(log[2])/simulator.timeout)
        if log[0] == SCV:s.append(float(log[2])/simulator.timeout)
        if log[0] == Orbital_Command:o.append(float(log[2])/simulator.timeout)
        if log[0] == MULE:M.append(float(log[2])/simulator.timeout)
        if log[0] == Extra_Supplies:e.append(float(log[2])/simulator.timeout)
    for log in simulator.log[:-1]:
        if log[0] == Barracks:b.append(float(log[2])/simulator.timeout)
    #if not Marine.number == len(t):print Marine.number, len(t)
    if len(t) == 0: x = 0
    else:x =  1 - sum(t)/len(t)
    if len(m) == 0: y = 0
    else:y =  1 - sum(m)/len(m)
    if len(s) == 0: z = 0
    else:z =  1 - sum(s)/len(s)
    if len(b) == 0: w = 0
    else:w =  (1 - sum(b)/len(b))*2
    if len(M) == 0: v = 0
    else:v = (1-sum(M)/len(M))
    #return len(t) + len(m)*4 + 0.1*len(s) + z + 5*len(o) + 2*len(M) + v + len(e)
    return len(t) + len(m)*4 + 0.1*len(s) + 5*len(o) + 2*len(M) + len(e) + x + y + v

def Evaluate(g):
    ct = count(1)
    Q = pipeline([(ct.next(), item) for item in g])
    endgame, extra = g[0].simulator.evaluate(Q)
    return endgame, extra

from copy import deepcopy, copy

class geno(list):
    def __init__(self, argv, simulator=None):
        list.__init__(self, [])
        self.normalize(argv)
        #list.__init__(self, argv)
        self._fitness = 0
        if not simulator == None:
            self.simulator = simulator
        else:
            self.simulator = self[0].simulator
        self.serialize()
        self.tag = '|'.join([item.object.name for item in self])
        self.availables = avGene(self)
    def normalize(self, argv):
        NoOfCC = 1
        NoOfOC = 0
        NoOfSD = 0
        NoOfES = 0
        HasRefinery = False
        TwoRefinery = False
        HasSCV = False
        for i in range(len(argv)):
            obj = argv[i].object
            if not HasRefinery and obj == Refinery:
                HasRefinery = True
            elif not HasSCV and obj == SCV:
                HasSCV = True
            elif HasRefinery and not TwoRefinery and obj == Refinery:
                if not HasSCV:
                    continue
                TwoRefinery = True
            if TwoRefinery and obj == Refinery:
                continue
            if obj == Command_Center:
                NoOfCC += 1
            elif obj == Orbital_Command or obj == Planetary_Fortress:
                NoOfOC += 1
            elif obj == Supply_Depot:NoOfSD += 1
            elif obj == Extra_Supplies:NoOfES += 1
            if NoOfOC > NoOfCC:
                print 'problem!!! NoOfOC %d NoOfCC %d' % (NoOfOC, NoOfCC)
                print [a.object.name for a in argv]
                continue
            if NoOfES > NoOfSD:
                #print 'problem!!! NoOfES %d NoOfSD %d' % (NoOfES, NoOfSD)
                #print [a.object.name for a in argv]
                raise Anomaly
                continue
            self.append(argv[i])
    def mutate(self):pass
    def crossover(self, other):pass
    def random(self):
        shuffle(self.availables)
        return self.availables[0]
    def fitness(self):
        if not self._fitness == 0:
            return self._fitness
        else:
            self._fitness = Fitness(self[0].simulator)
            return self._fitness
    def serialize(self):
        self.nodes = []
        bdReq = set([])
        bdPvd = set([Command_Center])
        PopReq = 0
        PopAvl = simulator.InitialPopulation - 6
        NoFreeBarracks = 0
        NoFreeFactories = 0
        NoFreeStarports = 0
        NoOfCC = 1
        NoOfSD = 0
        for i in range(len(self)):
            obj = self[i].object
            if obj == Barracks:NoFreeBarracks += 1
            if obj == Barracks_Tech_Lab: NoFreeBarracks += -1
            if obj == Barracks_Reactor: NoFreeBarracks += -1
            if obj == Factory:NoFreeFactories += 1
            if obj == Factory_Tech_Lab: NoFreeFactories += -1
            if obj == Factory_Reactor: NoFreeFactories += -1
            if obj == Starport:NoFreeStarports += 1
            if obj == Starport_Tech_Lab:NoFreeStarports += -1
            if obj == Starport_Reactor: NoFreeStarports += -1
            if obj == Command_Center: NoOfCC += 1
            if obj == Orbital_Command: NoOfCC += -1
            if obj == Planetary_Fortress: NoOfCC += -1
            if obj == Extra_Supplies:
                PopAvl += 8
                NoOfSD += -1
            if issubclass(obj.__class__, (RBUT.building, RBUT.tech)):
                bdPvd |= set([obj])
                if obj == Supply_Depot:
                    PopAvl += 8
                    NoOfSD += 1
                elif obj == Command_Center:
                    PopAvl += 11
            elif issubclass(obj.__class__, RBUT.unit ):
                PopAvl = PopAvl - obj.PopReq
            else:
                print '!!!!!!!'
                print obj.name, obj.__class__
            if PopAvl < 0:
                raise PopulationAnomaly
                #print 'population anomaly detected in build order', i  
                #print str(self)
            if NoFreeBarracks <= 0:
                if Barracks in bdPvd: bdPvd.remove(Barracks) 
            if NoFreeFactories <= 0:
                if Factory in bdPvd: bdPvd.remove(Factory)
            if NoFreeStarports <= 0:
                if Starport in bdPvd: bdPvd.remove(Starport)
            self.nodes.append({'PopAvl':PopAvl, 'bdPvd':bdPvd.copy(), 'NFB':NoFreeBarracks, 'NFF':NoFreeFactories, 'NFS':NoFreeStarports, 'NCC':NoOfCC, 'NSD':NoOfSD})
        idx = range(len(self))
        idx.reverse()
        NoNeedBarracks = 0
        NoNeedFactories = 0
        NoNeedStarports = 0
        CCNeeded = 0
        NoOfES = 0
        for i in idx:
            obj = self[i].object
            if obj == Barracks:NoNeedBarracks = max(0, NoNeedBarracks -1)
            if obj == Barracks_Tech_Lab: NoNeedBarracks += 1
            if obj == Barracks_Reactor: NoNeedBarracks += 1
            if obj == Factory:NoNeedFactories = max(0, NoNeedFactories -1)
            if obj == Factory_Tech_Lab: NoNeedFactories += 1
            if obj == Factory_Reactor: NoNeedFactories += 1
            if obj == Starport:NoNeedStarports = max(0, NoNeedStarports -1)
            if obj == Starport_Tech_Lab:NoNeedStarports += 1
            if obj == Starport_Reactor: NoNeedStarports += 1
            if obj == Command_Center: CCNeeded = max(0, CCNeeded-1)
            if obj == Orbital_Command: CCNeeded += 1
            if obj == Planetary_Fortress: CCNeeded += 1
            if obj == Extra_Supplies:
                PopReq = max(0, PopReq-8)
                NoOfES += 1
            if issubclass(obj.__class__, (RBUT.building, RBUT.tech)):
                if isinstance(obj.BuildingReq, (list,tuple)):
                    bdReq |= set(obj.BuildingReq)
                else:
                    bdReq |= set([obj.BuildingReq])
                bdReq = bdReq - set([obj])
                if obj == Supply_Depot:
                    PopReq = max(0, PopReq-8)
                    NoOfES = max(0, NoOfES-1)
                elif obj == Command_Center:
                    PopReq = max(0, PopReq-11)
            elif issubclass(obj.__class__, RBUT.unit):
                if isinstance(obj.BuildingReq, (list,tuple)):
                    bdReq |= set(obj.BuildingReq)
                else:
                    bdReq |= set([obj.BuildingReq])
                PopReq += obj.PopReq
            else:
                print obj.name
            self.nodes[i].update({'PopReq':PopReq,  'bdReq':(bdReq - set([None])).copy(), 'NNB':NoNeedBarracks, 'NNF':NoNeedFactories, 'NNS':NoNeedStarports, 'CCN':CCNeeded, 'NES':NoOfES})

    def __str__(self):
        ct = count(1)
        return '\n'.join(['%d %s' % (ct.next(), item.name) for item in self])
            

def TheMaker(simulator, geno, allowed):
    avGene.allowed = allowed
    P = geno([], simulator=simulator)
    new = P.mutate().mutate()
    avGene.allowed = default
    return new
    #while True:
        #it = P.random()
        #P = geno(P + [it])
        #endgame, extra = Evaluate(P)
        #if endgame: 
            #if extra > 0: #reaching the end time
                #P = geno(P[:-1*extra], simulator=simulator)
            #break
        #else: #Not reaching the end time
            #if extra == 0:
                #continue
            #else:
                #P = geno(P[:-1*extra], simulator=simulator)
                #continue
    #return geno(P, simulator=simulator)



class SPmuta(object):
    def mutate(self):
        try:
            simulator = self.simulator
        except:
            simulator = self[0].object.s
        new = self._mutate()
        ct1 = count(1)
        ct2 = count(1)
        while True:
            simulator.restart()
            endgame, extra = Evaluate(new)
            if not endgame:
                if extra == 0:
                    rdit = choice(new.availables)
                    #print [b.name for b in new], rdit.name, [b.name for b in new.availables]
                    new.append(rdit)
                    new = self.__class__(new)
                    continue
                else:
                    new = self.__class__(new[:-1*extra])
                    #if not endgame and extra > 0:
                    if ct2.next() > 10: 
                        print "BBBBBBB: ", extra
                        print str(self) #str(self.__class__(new.availables))
                        print "possible choices:"
                        print str(self.__class__(new).availables)
                        print "A plausible mutation"
                        print str(new)
                        print 'Minerals: ', self.simulator.mineral, self.simulator.time, self.simulator.population
                        print new[-1*extra].object.name
                        print simulator.queue
                        raise Exit
                #new = self._mutate()
                continue
            elif endgame and extra <= 1:
                new = self.__class__(new)
                new.fitness()
                return new
            elif endgame and extra > 1:
                #print "I shouldn't be here!" 
                if ct1.next() > 10: 
                    print "AAAAAAA: ", extra#str(self.__class__(new.availables))
                    print str(self)
                    print "possible choices:"
                    print str(self.__class__(new.availables))
                    print "A plausible mutation"
                    print str(new)
                    print 'Minerals: ', self.simulator.mineral, self.simulator.time
                    raise Exit
                new = self.__class__(new[:-1*extra])
            #if not endgame and not extra == 0:continue
            else:
                raise Exit
    def _mutate(self):
        if len(self) == 0:# mutate a size 0 geno to a size 1
            rdit = self.random()
            return self.__class__([rdit])
        elif len(self) ==1: # mutate a size 1 geno to a random sth else
            ct = count()
            while True:
                if ct.next() > 10:
                    print "Too many steps trying to find a mutation to a single one"
                    print self[0].name
                new = self.random()
                if not new.name == self[0].name:
                    return self.__class__([new])
        else:
            i = choice(range(1,len(self)))
            #print 'Mutation point ', i
            firsthalf = self[:i]
            if len(self) > i+1:
                secondhalf = self[i+1:]
            elif len(self) == i+1:
                secondhalf = []
            if not self[i].name == self[i-1].name:
                if i > 1:
                    PopAvl = self.nodes[i-2]['PopAvl']
                    bdPvd = self.nodes[i-2]['bdPvd']
                else:
                    PopAvl = self.simulator.InitialPopulation - 6
                    bdPvd = [Supply_Depot, Refinery]
                if issubclass(self[i].object.__class__, RBUT.unit):
                    if self[i].object.PopReq <= PopAvl and set(self[i].object.BuildingReq) <= set(bdPvd):
                        try:
                            return self.__class__(firsthalf[:-1] + [self[i], self[i-1]] + secondhalf)
                        except:pass
                    #else:
                        #print self[i].object.PopReq, PopAvl
                elif issubclass(self[i].object.__class__, RBUT.building):
                    if self[i].object in bdPvd:
                        return self.__class__(firsthalf[:-1] + [self[i], self[i-1]] + secondhalf)
                    #else:
                        #print self[i].object, [b.name for b in bdPvd]
                elif issubclass(self[i].object.__class__, RBUT.tech):
                    if not self[i-1].object in set(self[i].object.BuildingReq)|set(self[i].object.BuildingBusy) :
                        return self.__class__(firsthalf[:-1] + [self[i], self[i-1]] + secondhalf)
                    #else:
                        #print self[i-1].object.name ,[b.name for b in set(self[i].object.BuildingReq)|set(self[i].object.BuildingBusy)]
                else:
                    print '!!!!!!!!', self[i].object.name
            ct = count(0)
            while True:
                firstpart = self.__class__(firsthalf)
                new = firstpart.random()
                if new.name == self[i].name: continue
                if new.object == Orbital_Command:
                    if not secondhalf == []:
                        if self.nodes[i-1]['NCC'] - self.nodes[i+1]['CCN'] < 1:continue
                    else:
                        if self.nodes[i-1]['NCC'] < 1:continue
                if new.object == Extra_Supplies:
                    if not len(self) == i+1:
                        if self.nodes[i-1]['NSD'] - self.nodes[i+1]['NES'] < 1:
                            continue
                    else:
                        if self.nodes[i-1]['NSD'] < 1:
                            print 'NSD - NES', self.nodes[i]['NSD'] - self.nodes[i]['NES']
                            continue
                if ct.next() > 2*len(firstpart.availables): 
                    #print [t.name for t in firstpart.availables]
                    #print new.name, self[i].name
                    #print "Taking too many steps"
                    #print "Mutation point ", i
                    #print str(self)
                    return self._mutate()
                try: 
                    newbuild = self.__class__(firsthalf + [new] + secondhalf)
                except (PopulationAnomaly, Anomaly): continue
                if issubclass(new.object.__class__, RBUT.unit):
                    if new.object.PopReq <= self.nodes[i-1]['PopAvl'] and set(new.object.BuildingReq) <= self.nodes[i-1]['bdPvd']:
                        return self.__class__(firsthalf + [new] + secondhalf)
                elif issubclass(new.object.__class__, RBUT.building):
                    if set(new.object.BuildingReq) <= self.nodes[i-1]['bdPvd']: 
                        if not len(self) == i+1:
                            if (self.nodes[i-1]['bdPvd'] | set([new.object])) >= self.nodes[i+1]['bdReq']:
                                return self.__class__(firsthalf + [new] + secondhalf)
                            else:
                                continue
                        else:
                                return self.__class__(firsthalf + [new] + secondhalf)



class MPmuta(object):
    def mutate(self):pass

class SPcross(object):
    def crossover(self, other):
        simulator = self.simulator
        if self.tag == other.tag:
            return self.mutate().mutate()
        crosspoints = [(i, j) for i in range(len(self.nodes)) for j in range(len(other.nodes)) if other.nodes[j]['bdReq'] <= self.nodes[i]['bdPvd'] and other.nodes[j]['PopReq'] < self.nodes[i]['PopAvl'] and self.nodes[i]['NFB'] >= other.nodes[j]['NNB'] and self.nodes[i]['NFF'] >= other.nodes[j]['NNF'] and self.nodes[i]['NFS'] >= other.nodes[j]['NNS'] and self.nodes[i]['NCC'] >= other.nodes[j]['CCN'] and self.nodes[i]['NSD'] >= other.nodes[j]['NES']]
        #crosspoints2 = [(i, j) for i in range(len(self.nodes)) for j in range(len(other.nodes)) if self.nodes[i]['bdReq'] <= other.nodes[j]['bdPvd'] and self.nodes[i]['PopReq'] < other.nodes[j]['PopAvl']]
        #return crosspoints
        #crosspoints.sort(key = lambda x: abs(x[0]-x[1])*sum(x))
        #try:
        if len(crosspoints) == 0:
            #print '0 crosspoint found!'
            #print str(self)
            #print str(other)
            return other.mutate()
        else:
            (i,j) = choice(crosspoints)
        #except IndexError:
            #for i in range(min(len(self), len(other))):
                #print '%d: %s (%d)\t%s (%d)' % (i, self[i].object, self.nodes[i]['PopAvl'], other[i].object, other.nodes[i]['PopReq'])
        #(i,j) = choice(crosspoints[:len(crosspoints)/2])
        #print (i,j), self.nodes[i]['NCC'], other.nodes[j]['CCN']
        length = max(len(self), len(other))
        first = self[:i+1]
        second = other[j:]
        new = first + second
        if len([r for r in new if r.object == Refinery]) >= 2:
            RefineryLimit = 2
            ct = count(1)
            notes = []
            for k in range(len(new)):
                if new[k].object == Refinery:
                    if ct.next() > RefineryLimit:notes.append(k)
                elif new[k].object == Command_Center:
                    RefineryLimit += 2
            notes.sort(reverse=True)
            for l in notes:
                new.pop(l)


        simulator.restart()
        endgame, extra = Evaluate(new)
        if extra > 0:
            if endgame: 
                new = self.__class__(new[:-1*extra])
                new.fitness()
                return new
            if not endgame:
                print "We have a problem.", (i,j), self.nodes[i]['NSD'], other.nodes[j]['NES']#self.nodes[i]['PopAvl'], other.nodes[j]['PopReq']
                print [o.name for o in self.nodes[i]['bdPvd']]
                print [o.name for o in other.nodes[j]['bdReq']]
                self.simulator.verbose = True
                self.simulator.restart()
                for i in range(min(len(self), len(other))):
                    try:
                        print '%d: %s (%d) (%d)\t%s (%d) (%d)' % (i, self[i].object, self.nodes[i]['PopAvl'],self.nodes[i]['NSD'], other[i].object, other.nodes[i]['PopReq'], other.nodes[i]['NES'])
                    except:
                        print 'problemic i: ', i
                print len(new)
                print str(self.__class__(new))
                print Evaluate(new)
                sys.exit(0)
                return self

        if (not endgame) and extra == 0:
            new = self.__class__(new)
            return new.crossover(self.mutate())
        if endgame and extra == 0:
            new = self.__class__(new)
            new.fitness()
            return  new


class MPcross(object):
    def crossover(self, other):pass

def RandomMaker(genotype, simulator):
    yield genotype([], simulator=simulator).mutate()

def SingleTournament(grp):
    l = len(grp)
    shuffle(grp)
    a = sorted(grp[:l/2],key = lambda x:x.fitness())[-1]
    b = sorted(grp[l/2:],key = lambda x:x.fitness())[-1]
    grp.append(a.crossover(b))
    grp.append(b.crossover(a))
    grp.append(choice([a,b]).mutate())
    return heapq.nlargest(l, grp, key = lambda x:x.fitness())

def DoubleTournament(Grps):
    l = len(Grps)
    idx = range(l)
    i = choice(idx)
    j = i
    while j == i:
        j = choice(idx)
    a = max(Grps[i], key = lambda x:x.fitness())
    b = max(Grps[j], key = lambda x:x.fitness())
    def least(g):
        return min(g, key = lambda x:x.fitness()).fitness()
    gmin = heapq.nsmallest(2, Grps, key = least)
    gmin[0].sort(key = lambda x:x.fitness())
    gmin[1].sort(key = lambda x:x.fitness())
    gmin[0][0] = a
    gmin[1][0] = b
    return True

    


if __name__ == '__main__':
    import heapq
    class DNA(SPcross, SPmuta, geno):pass
    from ProgressBar import progressBar
    from terran import *

    Timeout = 330
    simulator = terran(Timeout)
    simulator.verbose = False

    #P = TheMaker(simulator, DNA, set([SCV, Supply_Depot, Barracks, Orbital_Command, MULE ]))
    #Q = TheMaker(simulator, DNA, set([SCV, Refinery, Supply_Depot, Barracks, Barracks_Tech_Lab, Marauder]))
    #print str(P)
    #print str(Q)
    #while not raw_input() == 'q':
        #P, Q = P.crossover(Q), Q.crossover(P)
        #P = P.mutate()
        #print str(P)
        #print str(Q)

    #import sys
    #sys.exit(0)
    try:
        P = TheMaker(simulator, DNA, set([SCV, Supply_Depot, Barracks, Orbital_Command, MULE ]))
        Q = TheMaker(simulator, DNA, set([SCV, Refinery, Supply_Depot, Barracks, Barracks_Tech_Lab, Marauder]))
        R = TheMaker(simulator, DNA, set([SCV, Supply_Depot, Barracks, Orbital_Command, Extra_Supplies]))

        Np = 80
        population = []
        generations = count(1)
        ct = count()
        while ct.next() < Np/2 + 2:
            population.append(P.mutate())
            population.append(Q.mutate())
            population.append(R.mutate())
        population = heapq.nlargest(Np, population, key = lambda g: g.fitness())
        maxfitness = population[0].fitness()
        lastmax = maxfitness
        n = 0
        while n < 200:
            for j in range(Np/2):
                #print 'crossover:'
                population.append(population[2*j].crossover(population[2*j+1]))
            for i in range(Np):
                #print 'mutate:'
                population.append(population[i].mutate())

            uniqness = {}
            for i in range(len(population)):
                build = population[i]
                if not uniqness.has_key(build.tag):
                    uniqness[build.tag] = build
                else:
                    population[i] = build.mutate()

            population = heapq.nlargest(Np, population, key = lambda g: g.fitness())
            maxfitness = population[0].fitness()
            minfitness = population[-1].fitness()
            if maxfitness == lastmax:
                n += 1
            else:
                lastmax = maxfitness
                n = 0
            print generations.next(), maxfitness, minfitness

        print 'exit:\n', population[0]
        #from pickle import dump
        #dump(population, f, -1)
        with open('Marauder%s.dat' % Timeout, 'w') as f:
            for i in range(Np):
                f.write('\n%d Marauders and %d Marine in %d:%d min:%s\n' % (len([o for o in population[i] if o.object == Marauder]),len([o for o in population[i] if o.object == Marine]), Timeout/60, Timeout % 60, population[i].fitness()))
                f.write(population[i].tag+'\n')
                f.write(str(population[i]))
    except (KeyboardInterrupt, SystemExit):
    #except:
        for i in range(3):
            print str(population[i])
        #rollback()

    #for p in population:
        #print ''
        #print str(p)





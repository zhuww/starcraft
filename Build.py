from RBUT import *
from zerg import *

def TestBuild(build, Timing, KeyPoint, KeyUnit):
    m = []
    g = []
    t = []
    simulator = zerg(0.5)
    build = build(simulator, Timing)
    def run(simulator, m, g, t):
        m.append(simulator.mineral) 
        g.append(simulator.gas) 
        t.append(simulator.time)
        build.make()
        m.append(simulator.mineral) 
        g.append(simulator.gas) 
        t.append(simulator.time)
        m.append(simulator.mineral) 
        g.append(simulator.gas) 
        t.append(simulator.queue[0][0])

    Hatchery.run()
    simulator.Mining()
    simulator.mainloop(300., run, simulator, m, g, t)
    for log in simulator.log:
        if log[0]== KeyPoint:
            return (log[2]+log[3], KeyUnit.number)

def Cancel1Extractor(simulator, Timing):
    Queue1 = []
    def condition1():
       return  simulator.mineral > 75.
    Cancel1 = Combo([ (1, NumberItem(Extractor, simulator, 1)), (2, NumberItem(Drone, simulator, 1)), (3,CancelItem(Extractor, simulator)) ])
    Queue1.append((1,NumberItem(Drone, simulator, 4)))
    Queue1.append((2,NumberItem(Overlord, simulator, 1)))
    Queue1.append((3,ConditionItem(Cancel1, simulator, condition1)))
    Queue1.append((5,NumberItem(Drone, simulator, 2)))
    Queue1.append((6,NumberItem(Spawning_Pool,simulator, 1)))
    Queue1.append((7,NumberItem(Drone, simulator, 5)))
    Queue1.append((8,Item(Metabolic_Boost, simulator)))
    Queue1.append((9,NumberItem(Queen, simulator, 1)))
    Queue1.append((10,NumberItem(Overlord, simulator, 1)))
    Queue1.append((11,NumberItem(Zergling, simulator, 'IDF')))
    PQ = pipeline(Queue1)
    Queue2 = []
    Queue2.append((4,TimingItem(HavestGas(simulator), simulator, Timing)))
    def condition2():
        return simulator.gas >= 100
    Queue2.append((5,ConditionItem(sendtogeyser(simulator, -3), simulator, condition2)))
    PQ2 = pipeline(Queue2)
    WF = workflow([PQ2, PQ])
    return WF


def Cancel2Extractor(simulator, Timing):
    Queue1 = []
    Queue1.append((4,TimingItem(HavestGas(simulator), simulator, Timing)))
    def condition2():
        return simulator.gas >= 100
    Queue1.append((5,ConditionItem(sendtogeyser(simulator, -3), simulator, condition2)))
    PQ1 = pipeline(Queue1)
    Queue2 = []
    def condition1():
       return  simulator.mineral > 105.
    Cancel2 = Combo([ (1, NumberItem(Extractor, simulator, 2)), (2, NumberItem(Drone, simulator, 2)), (3,CancelItem(Extractor, simulator)),(4,CancelItem(Extractor, simulator)) ])
    Queue2.append((1,NumberItem(Drone, simulator, 4)))
    Queue2.append((2,NumberItem(Overlord, simulator, 1)))
    Queue2.append((3,ConditionItem(Cancel2, simulator, condition1)))
    Queue2.append((5,NumberItem(Drone, simulator, 2)))
    Queue2.append((6,NumberItem(Spawning_Pool,simulator, 1)))
    Queue2.append((7,NumberItem(Drone, simulator, 4)))
    Queue2.append((8,Item(Metabolic_Boost, simulator)))
    Queue2.append((9,NumberItem(Queen, simulator, 1)))
    Queue2.append((10,NumberItem(Overlord, simulator, 1)))
    Queue2.append((11,NumberItem(Zergling, simulator, 'IDF')))
    PQ2 = pipeline(Queue2)
    WF = workflow([PQ1, PQ2])
    return WF


def NoExtractor(simulator, Timing):
    Queue1 = []
    Queue1.append((4,TimingItem(HavestGas(simulator), simulator, Timing)))
    def condition2():
        return simulator.gas >= 100
    Queue1.append((5,ConditionItem(sendtogeyser(simulator, -3), simulator, condition2)))
    PQ1 = pipeline(Queue1)
    Queue2 = []
    #def condition1():
       #return  simulator.mineral > 105.
    #Cancel2 = Combo([ (1, NumberItem(Extractor, simulator, 2)), (2, NumberItem(Drone, simulator, 2)), (3,CancelItem(Extractor, simulator)),(4,CancelItem(Extractor, simulator)) ])
    Queue2.append((1,NumberItem(Drone, simulator, 4)))
    #Queue2.append((2,ConditionItem(Cancel2, simulator, condition1)))
    Queue2.append((3,NumberItem(Overlord, simulator, 1)))
    Queue2.append((5,NumberItem(Drone, simulator, 3)))
    Queue2.append((6,NumberItem(Spawning_Pool,simulator, 1)))
    Queue2.append((7,NumberItem(Drone, simulator, 5)))
    Queue2.append((8,Item(Metabolic_Boost, simulator)))
    Queue2.append((9,NumberItem(Queen, simulator, 1)))
    Queue2.append((10,NumberItem(Overlord, simulator, 1)))
    Queue2.append((11,NumberItem(Zergling, simulator, 'IDF')))
    PQ2 = pipeline(Queue2)
    WF = workflow([PQ1, PQ2])
    return WF


def RoachBuild(simulator, Timing):
    Queue1 = []
    Queue1.append((4,TimingItem(HavestGas(simulator), simulator, Timing)))
    #def condition2():
        #return simulator.gas >= 100
    #Queue1.append((5,ConditionItem(sendtogeyser(simulator, -3), simulator, condition2)))
    PQ1 = pipeline(Queue1)
    Queue2 = []
    Queue2.append((1,NumberItem(Drone, simulator, 4)))
    #Queue2.append((2,ConditionItem(Cancel2, simulator, condition1)))
    Queue2.append((3,NumberItem(Overlord, simulator, 1)))
    Queue2.append((5,NumberItem(Drone, simulator, 3)))
    Queue2.append((6,NumberItem(Spawning_Pool,simulator, 1)))
    Queue2.append((7,NumberItem(Drone, simulator, 5)))
    Queue2.append((8,Item(Roach_Warren, simulator)))
    Queue2.append((9,NumberItem(Queen, simulator, 1)))
    Queue2.append((10,NumberItem(Overlord, simulator, 1)))
    #Queue2.append((11,NumberItem(Drone, simulator, 4)))
    Queue2.append((11,NumberItem(Drone, simulator, 2)))
    Queue2.append((12,NumberItem(Roach, simulator, 'IDF')))
    PQ2 = pipeline(Queue2)
    WF = workflow([PQ1, PQ2])
    return WF




def BanelingRush(simulator, Timing):
    Queue1 = []
    Queue1.append((4,TimingItem(HavestGas(simulator), simulator, Timing)))
    Queue1.append((11,NumberItem(Baneling, simulator, 'IDF')))
    def condition1():
       return  simulator.mineral > 75.
    Cancel1 = Combo([ (1, NumberItem(Extractor, simulator, 1)), (2, NumberItem(Drone, simulator, 1)), (3,CancelItem(Extractor, simulator)) ])
    PQ1 = pipeline(Queue1)
    Queue2 = []
    Queue2.append((1,NumberItem(Drone, simulator, 4)))
    Queue2.append((3,NumberItem(Overlord, simulator, 1)))
    Queue2.append((4,ConditionItem(Cancel1, simulator, condition1)))
    Queue2.append((5,NumberItem(Drone, simulator, 2)))
    Queue2.append((6,NumberItem(Spawning_Pool,simulator, 1)))
    Queue2.append((7,NumberItem(Drone, simulator, 4)))
    Queue2.append((8,Item(Baneling_Nest, simulator)))
    Queue2.append((9,NumberItem(Queen, simulator, 1)))
    Queue2.append((10,NumberItem(Overlord, simulator, 1)))
    Queue2.append((11,NumberItem(Zergling, simulator, 'IDF')))
    PQ2 = pipeline(Queue2)
    WF = workflow([PQ1, PQ2])
    return WF


def TwoBase(simulator, Timing):
    Queue1 = []
    Queue1.append((4,TimingItem(HavestGas(simulator), simulator, Timing)))
    def condition2():
        return simulator.gas >= 100
    #Queue1.append((5,ConditionItem(sendtogeyser(simulator, -3), simulator, condition2)))
    #Queue1.append((5,ConditionItem(Lair, simulator, condition2)))
    PQ1 = pipeline(Queue1)
    Queue2 = []
    def condition1():
       return  simulator.mineral > 75.
    Cancel1 = Combo([ (1, NumberItem(Extractor, simulator, 1)), (2, NumberItem(Drone, simulator, 1)), (3,CancelItem(Extractor, simulator)) ])
    Queue2.append((1,NumberItem(Drone, simulator, 4)))
    Queue2.append((2,NumberItem(Overlord, simulator, 1)))
    Queue2.append((3,ConditionItem(Cancel1, simulator, condition1)))
    Queue2.append((5,NumberItem(Drone, simulator, 3)))
    Queue2.append((6,NumberItem(Spawning_Pool, simulator, 1)))
    Queue2.append((7,NumberItem(Drone, simulator, 4)))
    Queue2.append((8,NumberItem(Hatchery,simulator, 1)))
    Queue2.append((9,NumberItem(Queen, simulator, 1)))
    Queue2.append((10,NumberItem(Spine_Crawler, simulator, 1)))
    Queue2.append((11,NumberItem(Drone, simulator, 2)))
    Queue2.append((12,NumberItem(Overlord, simulator, 1)))
    Queue2.append((13,NumberItem(Queen, simulator, 1)))
    Queue2.append((14,ConditionItem(Lair, simulator, condition2)))
    Queue2.append((15,NumberItem(Drone, simulator, 'IDF')))
    PQ2 = pipeline(Queue2)
    WF = workflow([PQ1, PQ2])
    return WF

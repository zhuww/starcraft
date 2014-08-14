from RBUT import *
from zerg import *
from Build import *
import time,sys
import matplotlib
import matplotlib.pyplot as plt
from numpy import array
from plot import *

oldStdout = sys.stdout
sys.stdout = open("Output.log", "w")


CancelOne = lambda Timing: TestBuild(Cancel1Extractor, Timing, Metabolic_Boost, Zergling)
CancelTwo = lambda Timing: TestBuild(Cancel2Extractor, Timing, Metabolic_Boost, Zergling)
NoCancel = lambda Timing: TestBuild(NoExtractor, Timing, Metabolic_Boost, Zergling)
RoachBoom = lambda Timing: TestBuild(RoachBuild, Timing, Roach, Roach)
BanelingBuild = lambda Timing: TestBuild(BanelingRush, Timing, Baneling_Nest, Baneling)
TwoBaseZerg = lambda Timing: TestBuild(TwoBase, Timing, Spawning_Pool, Zergling)
TwoBaseDefense = lambda Timing: TestBuild(TwoBase, Timing, Hatchery, Drone)

#data = [(x, CancelOne(x)) for x in [ 70, 75, 80, 85, 90, 95, 100]]
#data = [(x, CancelTwo(x)) for x in [ 80, 85, 90, 95, 100, 105]]
#data = [(x, NoCancel(x)) for x in [  80, 85, 90, 95, 100, 105, 110, 115, 120, 125]]
#data = [(x, RoachBoom(x)) for x in [80, 90, 100, 110, 120, 130, 140, 150, 155, 160, 170, 175, 180]]
#data = [(x, BanelingBuild(x)) for x in [80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]]
data = [(x, TwoBaseDefense(x)) for x in [80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]]

sys.stdout = oldStdout

#for x in [80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]:
    #print (x, TwoBaseDefense(x)) 

for test in data:
    print test

#print 'by 5min, %i Zerglings were produced.' % Zergling.number

#for log in simulator.log:
    #print '%s: %s took %s' % (log[0].name, log[2], log[3])




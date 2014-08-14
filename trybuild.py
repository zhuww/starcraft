from terran import *
from GP import Evaluate, geno, avGene, GeneSelector
Timeout = 210
simulator = terran(Timeout)

build = [
SCV,
SCV,
SCV,
SCV,
Supply_Depot,
SCV,
SCV,
SCV,
Refinery,
Barracks,
Barracks_Reactor,
Marine,
Marine,
]
P = []
i = 0
for b in build:
    P.append(Item(b, simulator))
    i+=1
g = geno(P)
Endgame, extra, Qleft = Evaluate(g)
print Endgame, extra, Qleft[1].name
#print simulator.queue[0][1][0].name
#print SCV.number, SCV.occupied
#print [a.name for a in g.availables]
#print [a.name for a in avGene.allowed]
#print [a.name for a in avGene(g)]
print g.fitness()
#print Factory.number, Factory.occupied
#print Factory.List

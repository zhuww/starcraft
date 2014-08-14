from GP import *
#default.remove()
#default.remove()
if __name__ == '__main__':
    import heapq
    class DNA(SPcross, SPmuta, geno):pass
    from ProgressBar import progressBar
    from terran import *

    Timeout = 450
    simulator = terran(Timeout)
    simulator.verbose = False

    #O = TheMaker(simulator, DNA, [Orbital_Command, MULE, Barracks, Marine, Barracks_Reactor, Factory, Factory_Tech_Lab, Starport, Swap_Barracks_Starport_Reactor, Supply_Depot, SCV, Siege_Tech, Siege_Tank ], KeyUnit=Viking)
    #P = TheMaker(simulator, DNA, [Supply_Depot, SCV, SCV, SCV, Command_Center, Marine, Factory, Starport, Factory_Tech_Lab, Siege_Tank], KeyUnit=Viking)
    #Q = TheMaker(simulator, DNA, [SCV, SCV, Supply_Depot, Barracks, Factory, Refinery, Barracks_Tech_Lab, Marauder, Starport, Swap_Barracks_Factory_Tech_Lab, Barracks_Reactor, Supply_Depot, Siege_Tank, Swap_Barracks_Starport_Reactor, Viking, Viking], KeyUnit=Viking)
    #R = TheMaker(simulator, DNA, [Factory, Barracks_Reactor, Starport, Swap_Barracks_Starport_Reactor, Factory_Tech_Lab, Supply_Depot, Siege_Tank, Viking, SCV, Siege_Tech ], KeyUnit=Marine)
    #S = TheMaker(simulator, DNA, [Orbital_Command, Marine, Marine, Factory, MULE, Starport, Factory_Tech_Lab, Starport_Reactor, Extra_Supplies, Siege_Tank, Viking, Command_Center], KeyUnit=SCV)
    #T = TheMaker(simulator, DNA, [Refinery, Factory, Barracks_Tech_Lab, Marauder, Swap_Barracks_Factory_Tech_Lab, Barracks_Reactor, Siege_Tank, Starport, Swap_Barracks_Starport_Reactor, Siege_Tech, Supply_Depot, Viking, Command_Center], KeyUnit=Siege_Tank)
    #O = TheMaker(simulator, DNA, [Orbital_Command, Barracks,MULE, Marine, Barracks_Tech_Lab, Supply_Depot, SCV, Concussive_Shells, Marauder], KeyUnit=Marauder)
    #print 'O'
    #P = TheMaker(simulator, DNA, [Supply_Depot, SCV, SCV, SCV, Command_Center, Marine, Barracks, Barracks_Tech_Lab, Concussive_Shells], KeyUnit=Marauder)
    #print 'P'
    #Q = TheMaker(simulator, DNA, [Barracks, Supply_Depot, Barracks, Barracks_Tech_Lab, Marauder, Concussive_Shells, Supply_Depot ], KeyUnit=Marine)
    #print 'Q'
    #R = TheMaker(simulator, DNA, [Barracks_Reactor, Barracks, Barracks, Supply_Depot ], KeyUnit=Marine)
    #print 'R'
    #S = TheMaker(simulator, DNA, [Orbital_Command, SCV, SCV, Barracks, Barracks_Tech_Lab, MULE, Concussive_Shells, Extra_Supplies ], KeyUnit=Marauder)
    #print 'S'
    #T = TheMaker(simulator, DNA, [Barracks, Barracks_Tech_Lab, Marauder, Concussive_Shells, Supply_Depot ], KeyUnit=Marine)
    #print 'T'


    #print str(O)
    #print str(P)
    #print str(Q)
    #print str(R)
    #print str(S)
    #print str(T)
    #while not raw_input() == 'q':
        #P, Q = P.crossover(Q), Q.crossover(P)
        #P = P.mutate()
        #print str(P)
        #print str(Q)

    #import sys
    #sys.exit(0)
    try:
        O = TheMaker(simulator, DNA, [Orbital_Command, Barracks,MULE, Marine, Barracks_Tech_Lab, Supply_Depot, SCV, Concussive_Shells, Marauder], KeyUnit=Marauder)
        print 'O'
        P = TheMaker(simulator, DNA, [Supply_Depot, SCV, SCV, SCV, Marine, Barracks, Barracks_Tech_Lab, Concussive_Shells], KeyUnit=Marauder)
        print 'P'
        Q = TheMaker(simulator, DNA, [Barracks, Supply_Depot, Barracks, Barracks_Tech_Lab, Marauder, Concussive_Shells, Supply_Depot ], KeyUnit=Marine)
        print 'Q'
        R = TheMaker(simulator, DNA, [Barracks_Reactor, Barracks, Barracks, Supply_Depot ], KeyUnit=Marine)
        print 'R'
        S = TheMaker(simulator, DNA, [Orbital_Command, SCV, SCV, Barracks, Barracks_Tech_Lab, MULE, Concussive_Shells, Extra_Supplies ], KeyUnit=Marauder)
        print 'S'
        T = TheMaker(simulator, DNA, [Barracks, Barracks_Tech_Lab, Marauder, Concussive_Shells, Supply_Depot ], KeyUnit=Marine)
        print 'T'

        print 'Start from here'

        Np = 80
        population = [O,P,Q,R,S,T]
        generations = count(1)
        ct = count()
        while ct.next() < Np/2 + 2:
            population.append(O.mutate())
            population.append(P.mutate())
            population.append(Q.mutate())
            population.append(R.mutate())
            population.append(S.mutate())
            population.append(T.mutate())
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
        with open('MarineMarauder%s.dat' % Timeout, 'w') as f:
            for i in range(Np):
                f.write('\n%d Marine and %d Marauder %d:%d min:%s\n' % (len([o for o in population[i] if o.object == Marine]),len([o for o in population[i] if o.object == Marauder]), Timeout/60, Timeout % 60, population[i].fitness()))
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

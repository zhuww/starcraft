from GP import *
#default.remove(Marauder)
#default.remove(Marine)
if __name__ == '__main__':
    import heapq
    class DNA(SPcross, SPmuta, geno):pass
    from ProgressBar import progressBar
    from terran import *

    Timeout = 420
    simulator = terran(Timeout)
    simulator.verbose = False

    #O = TheMaker(simulator, DNA, [Orbital_Command, MULE, Factory, Factory_Tech_Lab, Siege_Tank ], KeyUnit=Marine)
    #P = TheMaker(simulator, DNA, [Barracks_Tech_Lab, Factory, Swap_Barracks_Factory_Tech_Lab ], KeyUnit=Siege_Tank)
    #Q = TheMaker(simulator, DNA, [Factory, Factory_Tech_Lab, Siege_Tank ], KeyUnit=Siege_Tank)
    #R = TheMaker(simulator, DNA, [Factory, Factory_Tech_Lab, Siege_Tech ], KeyUnit=Siege_Tank)
    #S = TheMaker(simulator, DNA, [Barracks_Tech_Lab, Factory, Swap_Barracks_Factory_Tech_Lab, Siege_Tech], KeyUnit=Siege_Tank)
    #T = TheMaker(simulator, DNA, [Factory, Factory_Tech_Lab, Siege_Tech], KeyUnit=Siege_Tank)
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
        O = TheMaker(simulator, DNA, [Orbital_Command, MULE, Factory, Factory_Tech_Lab, Siege_Tank ], KeyUnit=Marine)
        P = TheMaker(simulator, DNA, [Barracks_Tech_Lab, Factory, Swap_Barracks_Factory_Tech_Lab ], KeyUnit=Siege_Tank)
        Q = TheMaker(simulator, DNA, [Factory, Factory_Tech_Lab, Siege_Tank ], KeyUnit=Siege_Tank)
        R = TheMaker(simulator, DNA, [Factory, Factory_Tech_Lab, Siege_Tech ], KeyUnit=Siege_Tank)
        S = TheMaker(simulator, DNA, [Barracks_Tech_Lab, Factory, Swap_Barracks_Factory_Tech_Lab, Siege_Tech], KeyUnit=Siege_Tank)
        T = TheMaker(simulator, DNA, [Factory, Factory_Tech_Lab, Siege_Tech], KeyUnit=Siege_Tank)

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
        with open('Tank%s.dat' % Timeout, 'w') as f:
            for i in range(Np):
                f.write('\n%d Tanks and %d Marines in %d:%d min:%s\n' % (len([o for o in population[i] if o.object == Siege_Tank]),len([o for o in population[i] if o.object == Marine]), Timeout/60, Timeout % 60, population[i].fitness()))
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

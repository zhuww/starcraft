from GP import *
#default.remove(Marauder)
#default.remove(Marine)

if __name__ == '__main__':
    import heapq
    class DNA(SPcross, SPmuta, geno):pass
    from ProgressBar import progressBar
    from datetime import *

    Timeout = 360
    simulator = terran(Timeout)
    simulator.verbose = False

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
        Ng = 20
        Groups = []
        O, P, Q, R, S, T, U = [], [], [], [], [], [], []
        for i in range(Ng):
            O.append(TheMaker(simulator, DNA, [SCV, Supply_Depot, Barracks, Refinery, Factory, Factory_Tech_Lab, Siege_Tank, Siege_Tank ]))
            P.append(TheMaker(simulator, DNA, [SCV, Supply_Depot, Barracks, Refinery, Orbital_Command, MULE, Factory, Factory_Tech_Lab, Siege_Tank ]))
            Q.append(TheMaker(simulator, DNA, [SCV, Supply_Depot, Barracks, Refinery, Barracks_Tech_Lab, Factory, Swap_Barracks_Factory_Tech_Lab, Siege_Tech, Siege_Tank]))
            R.append(TheMaker(simulator, DNA, [SCV, Supply_Depot, Barracks, Refinery, Orbital_Command, Factory, Extra_Supplies, Siege_Tank ]))
            S.append(TheMaker(simulator, DNA, [SCV, Refinery, Supply_Depot, Barracks, Barracks_Tech_Lab, Factory, Siege_Tank, Swap_Barracks_Factory_Tech_Lab, Siege_Tank, Siege_Tank]))
            T.append(TheMaker(simulator, DNA, [SCV, Refinery, Supply_Depot, Barracks, Factory, Factory_Tech_Lab, Siege_Tech, Siege_Tank]))
            U.append(TheMaker(simulator, DNA, [SCV, Refinery, Supply_Depot, Barracks, Factory, Factory_Tech_Lab, Siege_Tank, Siege_Tech ]))
            #V.append(TheMaker(simulator, DNA, default))
            #W.append(TheMaker(simulator, DNA, default))
            #X.append(TheMaker(simulator, DNA, default))
            #Y.append(TheMaker(simulator, DNA, default))
            #Z.append(TheMaker(simulator, DNA, default))
        Groups= [O, P, Q, R, S, T, U]

        ct = count()
        TotalSteps = 3000
        pb = progressBar(minValue = 0, maxValue=TotalSteps)
        i = ct.next()
        pb(0)
        past = datetime.now()
        while i < TotalSteps:
            pb(i)
            if i > 9 and i % 10 == 0:
                ETR = (datetime.now() - past).total_seconds()/3600./i*(TotalSteps - i)
                EHR = int(ETR)
                EMR = (ETR - EHR)*60
                print '\n','; '.join(['%d, %d' % (max(g, key = lambda x: x.fitness()).fitness(), min(g, key = lambda x: x.fitness()).fitness()) for g in Groups]), 'ETR:%dh:%dm' % (EHR, EMR), '\n'
                pb(i)
            unique(Groups)
            new = [SingleTournament(Lamarckican(g)) for g in Groups]
            Groups = new
            if i >=50 and i % 50 ==0: DoubleTournament(Groups)
            i = ct.next()

        Np = 15
        population = []
        for g in Groups:
            population += g
        population = heapq.nlargest(Np, population, key = lambda g: g.fitness())
        population.sort(key = lambda g: g.fitness())



        print 'exit:\n', population[0]
        #from pickle import dump
        #dump(population, f, -1)
        with open('Tank%s.txt' % Timeout, 'w') as f:
            for i in range(Np):
                f.write('\n%d Siege_Tanks and %d Marine in %d:%d min:%s\n' % (len([o for o in population[i] if o.object == Siege_Tank]),len([o for o in population[i] if o.object == Marine]), Timeout/60, Timeout % 60, population[i].fitness()))
                f.write(population[i].tag+'\n')
                f.write(str(population[i]))
    except (KeyboardInterrupt, SystemExit):
    #except:
        for i in range(3):
            Np = 3
            population = []
            for g in Groups:
                population += g
            population = heapq.nlargest(Np, population, key = lambda g: g.fitness())
            population.sort(key = lambda g: g.fitness())
            print str(population[i])
        #rollback()

    #for p in population:
        #print ''
        #print str(p)





from time import sleep
from RBUT import *

terren = race('terren')
protoss = race('protoss')
zerg = race('zerg')


class simulator(race):
    def __init__(self, race=terren):
        self.mineral = 0
        self.gas = 0
        self.population = 10
    def run(self):
        SCV = unit(50, 0, 17)
        SCV.number = 4
        SCV.produce()
        while True:
            sleep(0.5)
            print SCV.number
            if SCV.number == 5: break

if __name__ == '__main__':
    GameSpeed = 0.1
    sim = simulator()
    sim.run()

import RBUT 

def showReq(obj):
    #if isinstance(obj, RBUT.unit):
        #Building = obj.BuildingReq
    #elif isinstance(obj, RBUT.building):
        #Building = obj
    #else:
        #raise TypeError 
    time = obj.TimeReq
    mineral = 0.
    gas = 0.
    while not obj.BuildingReq == None:
        time += obj.TimeReq
        mineral += obj.MineReq
        gas += obj.GasReq
        print obj.name, obj.TimeReq
        obj = obj.BuildingReq
    return (mineral, gas, time)

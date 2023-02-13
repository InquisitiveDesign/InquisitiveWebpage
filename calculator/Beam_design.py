def beamd(bl,ns,nl,supportloc,supporttype,supportdirec,loadloc,loadtype,loaddirec,loadvalue):
    import math
    Num_support = int(ns)
    Num_load = int(nl)
    #Now for a simply supported beam
    Totload = 0
    for load in range(len(loadvalue)):
        if loaddirec[load] == "Downwards":
            Totload = Totload + loadvalue[load]
        elif loaddirec[load] == "Upwards":
            Totload = Totload - loadvalue[load]
    #For simply supported beam there are two equations 1st is force balance i.e. summation of load euals summation of reaction or support reaction force.
    #2nd equation is resultant moment of all forces and moment applied on the beam is zero at any support location.
    #Considering max support in this case as 2 so name R1 and R2.
    #considering moment eqn about 1st reaction force.
    loadmoment = 0
    for m in range(0,len(loadvalue)):
        if loaddirec[m] == "Downwards" and loadtype[m] == "Point":
            loadmoment = loadmoment - loadvalue[m]*(loadloc[m] - supportloc[0])
        elif loaddirec[m] == "Upwards" and loadtype[m] == "Point":
            loadmoment = loadmoment + loadvalue[m]*(loadloc[m] - supportloc[0])
        elif loaddirec[m] == "Clockwise" and loadtype[m] == "Moment":
            loadmoment = loadmoment - loadvalue[m]
        elif loaddirec[m] == "AntiClockwise" and loadtype[m] == "Moment":
            loadmoment = loadmoment + loadvalue[m]
    if supportdirec[1] == "Downwards" and supporttype[1] == "Pin":
        R2 = (1/(supportloc[1]-supportloc[0]))*loadmoment
    elif supportdirec[1] == "Upwards" and supporttype[1] == "Pin":
        R2 = (-1/(supportloc[1]-supportloc[0]))*loadmoment
    R1 = Totload - R2
    return [round(R1,3),round(R2,3)]

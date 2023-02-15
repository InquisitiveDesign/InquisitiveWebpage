def bearing_selector(bore_dia,RPM,VFC,HFC,AFC,Rotation_fact,yr,hr_eachdy):
    
    import math
    from calculator.my_bearing import my_bearing

    Fv = float(VFC)
    Fh = float(HFC)
    Fa = float(AFC)

    #total radial load
    Fr = math.sqrt((Fv)**2+(Fh)**2)
    
    #Determining the radial load factor by trial and error
    fafrratio = float(Fa/Fr)

    e_list = [0.22,0.24,0.27,0.31,0.37,0.44]
    X_factor = [1,0.56]
    Y_factor = [2,1.8,1.6,1.4,1.2,1,0]
    Fa_Co = [0.025,0.04,0.07,0.13,0.25,0.50]

    Y = 1.5  # avg assumed value of Y
    X = X_factor[1]

    #Rotation factor R = 1 (inner race rotates), R = 1.2 (outer race rotates)
    R = float(Rotation_fact)

    #Equivalent dynamic load (in kN)
    W = (X*R*Fr)+(Y*Fa)

    #load life relationship
    # Years of life (Y)
    # Operating time each day(OT) in hours
    #Life of a bearing Lhr(in hours)

    YR = float(yr)
    OT = float(hr_eachdy)
    N = float(RPM)

    #Life of a bearing Lrev(in million revolution)
    Lhr = (YR)*(OT)*365

    Lrev = Lhr*60*N

    #Basic dynamic radial load, C (kN)
    #Bearing index "n" for ball bearing
    n = float(1/3)

    #Dynamic load carrying capacity
    c = W*(Lrev/(10**6))**(n)
    
    b = float(bore_dia)

    my_bearing(c,b)
    faCoratio = float(Fa/my_bearing(c,b)[5])
    
    func_floor_value = math.floor(faCoratio)
    def final_comparision(mylist):
        segregation = {}
        for i in mylist:
            list_floor_value = math.floor(i)
            if list_floor_value == func_floor_value:
                diff = abs(faCoratio - i)
                segregation[i] = diff
            else:
                continue
        dictvalue = min(segregation.values())
        for key in segregation:
            if segregation[key] == dictvalue:
                return key

    index = Fa_Co.index(final_comparision(Fa_Co))
    e = e_list[index]       #approx value
    Fa_Co = [0.025,0.04,0.07,0.13,0.25,0.50]
    Y_factor = [2,1.8,1.6,1.4,1.2,1,0]
    if fafrratio > e:
        X = X_factor[1]
        smaller = []
        greater = []
        for r in Fa_Co:
            if faCoratio >= r:
                smaller.append(r)

            if faCoratio <= r:
                greater.append(r)

        if smaller == []:
            smaller.append(min(Fa_Co))

        if greater == []:
            greater.append(max(Fa_Co))
     
        faComin = max(smaller)
        faComax = min(greater)
        indxmin = Fa_Co.index(faComin)
        indxmax = Fa_Co.index(faComax)
        Ymin = Y_factor[indxmin]
        Ymax = Y_factor[indxmax]

        try:
            Y = Ymin+((Ymax-Ymin)/(faComax-faComin))*(faCoratio-faComin)
        except:
            Y = Ymin or Ymax
    
    elif fafrratio <= e:
        X = X_factor[0]
        Y = Y_factor[-1]

    #again equivalent dynamic load (in kN)
    W = (X*R*Fr)+(Y*Fa)
    cnew = W*(Lrev/(10**6))**(n)
    my_bearing(cnew,b)

    return [my_bearing(cnew,b)[0], my_bearing(cnew,b)[1], my_bearing(cnew,b)[2], my_bearing(cnew,b)[3], my_bearing(cnew,b)[4], my_bearing(cnew,b)[5], my_bearing(cnew,b)[6], my_bearing(cnew,b)[7]]
    

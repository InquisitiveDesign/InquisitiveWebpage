def shaft_combined(BM,TM,S,F,LT,Th,db,dr):
    import math
    # Values of shock and fatigue factors Kb and Kt
    KB = [1.5,2,3]    # combined shock and fatigue factor applied to bending moment
    KT = [1,1.5,3]    # combined shock and fatigue factor applied to torsional moment
    Mb = float(BM)
    Mt = float(TM)
    yi_st = float(S)
    fos = float(F)

    factor = LT
    if factor.upper() == "G":
        kb = KB[0]
        kt = KT[0]
    elif factor.upper() == "S":
        kb = KB[1]
        kt = KT[1]
    elif factor.upper() == "H":
        kb = KB[2]
        kt = KT[2]
    else:
        kb = 1
        kt = 1

    design_theory = Th
    if design_theory.upper() == "S":
        sh_yi = 0.5*yi_st
    elif design_theory.upper() == "D":
        sh_yi = 0.577*yi_st
    else:
        sh_yi = -1.0
        print("invalid input")

    maxp_sh_stress = (sh_yi/fos)

    design_basedon = db
    if design_basedon.upper() == "T":
        Meq = math.sqrt(((kb*Mb)**2)+((kt*Mt)**2))

    elif design_basedon.upper() == "B":
        Meq = (kb*Mb) + (math.sqrt(((kb*Mb)**2)+((kt*Mt)**2)))

    #else:
        #print("invalid input")

    C = float(dr)

    if C == 0:
        shaft_dia = round((16*Meq/((math.pi)*maxp_sh_stress))**(1./3.),2)
        return [shaft_dia, 0]

    elif C > 0 and C < 1:
        Outer_shaft_dia = round((16*Meq/((math.pi)*maxp_sh_stress*(1-(C**4))))**(1./3.),2)
        Inner_shaft_dia = round(Outer_shaft_dia*C,2)
        return [Outer_shaft_dia, Inner_shaft_dia]

def shaft_from_rigiditymodulus(Theta,G,TM,L,Rdia):
    import math
    theta_max = float(Theta)
    G = float(G)
    Mt = float(TM)
    Len = float(L)
    C = float(Rdia)


    if C == 0:
        shaft_dia = round(((584*Mt*Len)/(G*theta_max))**(1./4.),2)
        return [shaft_dia, 0]

    elif C > 0 and C < 1:
        Outer_shaft_dia = round(((584*Mt*Len)/(G*theta_max*(1-(C**4))))**(1./4.),2)
        Inner_shaft_dia = round(Outer_shaft_dia*C,2)
        return [Outer_shaft_dia, Inner_shaft_dia]

    else:
        shaft_dia = round(((584*Mt*Len)/(G*theta_max))**(1./4.),2)
        return [shaft_dia, 0]

def key_d(P,N,S,F,D,Th):
    import math
    power_in = float(P)
    Nspeed = float(N)
    yi_st = float(S)
    fos = float(F)
    shaftDia = float(D)
    design_theory = Th

    com_st = yi_st                 #considering compressive yield equal to tensile yield
    max_percs = float(com_st/fos)

    if design_theory == "S" or design_theory == "s":
        sh_st = 0.5*yi_st

    elif design_theory == "D" or design_theory == "d":
        sh_st = 0.577*yi_st

    else:
        print("invalid input")

    max_perss = float(sh_st/fos)   #max permissible shear stress
    omega = (2*(math.pi)*Nspeed/60)   #angular speed in rad/sec
    Mt = (power_in*(10**6)/(omega))   #Torque to be transmitted by the shaft to hub via key in N-mm
    B = float(shaftDia/4)          #Width and height (in mm) as per the standard industrial practice i.e 1/4th of shaft dia for square key
    H = float(shaftDia/4)
    keylen_ssbased = float(2*Mt/(max_perss*B*H))
    keylen_csbased = float(4*Mt/(max_percs*B*H))
    if keylen_ssbased >= keylen_csbased:
        L = keylen_ssbased

    elif keylen_ssbased < keylen_csbased:
        L = keylen_csbased

    return [L,B,H]

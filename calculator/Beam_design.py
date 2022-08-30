def beamd(BL, NS, NL):
    import math

    beam_length = float(BL)
    Num_support = int(NS)
    Num_load = int(NL)

    Support_type = []
    loc_supp = []
    Supp_direc = []
    for n in range(Num_support):
        Support_type.append()
        loc_supp.append()  # from left end of the beam in mm
        Supp_direc.append()

    Load_type = []
    loc_load = []
    load_direc = []
    load_val = []
    for i in range(Num_load):
        Load_type.append()
        loc_load.append()
        load_direc.append()
        load_val.append()

    # Now for a simply supported beam
    Totload = sum(load_val)

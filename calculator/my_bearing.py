def my_bearing(c,b,n):
    import math
    import xlrd         # run pip install xlrd on cmd, Reading an excel file using Python
    # Give the location of the file
    if n == float(1/3):
        loc = ("calculator/SKFballbearingcatalogue.xls")
    else:
        loc = ("calculator/SKF_single-row-cyl-rollerbearingcatalogue.xls")

# To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    i = 0
    Bearing_desigination = []
    Bore = []
    OD = []
    Width = []
    Cd = []
    Co = []
    Ref_Speed = []
    Lim_Speed = []

# Program extracting all rows
    while i < (int(sheet.nrows)-1):
        i = i + 1

        if float(sheet.cell_value(i,1)) == b and float(sheet.cell_value(i,4)) >= c:
            Bearing_desigination.append(sheet.cell_value(i,0))
            Bore.append(sheet.cell_value(i,1))
            OD.append(sheet.cell_value(i,2))
            Width.append(sheet.cell_value(i,3))
            Cd.append(sheet.cell_value(i,4))
            Co.append(sheet.cell_value(i,5))
            Ref_Speed.append(sheet.cell_value(i,6))
            Lim_Speed.append(sheet.cell_value(i,7))
            #print("Bearing_desigination ",sheet.cell_value(i,0),"Bore ",sheet.cell_value(i,1),"OD ",sheet.cell_value(i,2),"Width ",sheet.cell_value(i,3),"Cd ",sheet.cell_value(i,4),"Co ",sheet.cell_value(i,5),"Ref_Speed ",sheet.cell_value(i,6),"Lim_Speed ",sheet.cell_value(i,7))

    if Cd != []:
        m = Cd.index(min(Cd))

    elif Cd == []:
        i = 0
        #print("entered bore dia not available")
        while i < (int(sheet.nrows)-1):
            i = i + 1
            if float(sheet.cell_value(i,1)) != b and float(sheet.cell_value(i,4)) >= c:

                Bearing_desigination.append(sheet.cell_value(i,0))
                Bore.append(sheet.cell_value(i,1))
                OD.append(sheet.cell_value(i,2))
                Width.append(sheet.cell_value(i,3))
                Cd.append(sheet.cell_value(i,4))
                Co.append(sheet.cell_value(i,5))
                Ref_Speed.append(sheet.cell_value(i,6))
                Lim_Speed.append(sheet.cell_value(i,7))

        m = Cd.index(min(Cd))

    if n == float(1/3):
        return [Bearing_desigination[m], Bore[m], OD[m], Width[m], Cd[m], Co[m], Ref_Speed[m], Lim_Speed[m], c, "Ball Bearing"]
    else:
        return [Bearing_desigination[m], Bore[m], OD[m], Width[m], Cd[m], Co[m], Ref_Speed[m], Lim_Speed[m], c, "Roller Bearing"]
    

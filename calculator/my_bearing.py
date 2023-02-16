def my_bearing(c,b):
    import math
    import xlrd                                   # run pip install xlrd on cmd, Reading an excel file using Python
    loc = ("E:\Py4e\SKFbearingcatalogue.xls")     # Give the location of the file

# To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

#For row 0 and column 0
#print(sheet.cell_value(0, 0))
#Extracting number of rows
#print(sheet.nrows)
#Extracting number of columns
#print(sheet.ncols)
#n = range(sheet.nrows)
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
        print("entered bore dia not available")
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

    return [Bearing_desigination[m], Bore[m], OD[m], Width[m], Cd[m], Co[m], Ref_Speed[m], Lim_Speed[m]]

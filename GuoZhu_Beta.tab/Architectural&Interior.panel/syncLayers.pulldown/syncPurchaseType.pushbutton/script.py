# -*- coding: utf-8 -*-

from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

u_shape_collec = []
rhs_shape_collec = []
ang_shape_collec = []

# Creating collector instance and collecting all the stiffeners from the model
all_TempStr = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TemporaryStructure).WhereElementIsElementType()


# Loop through all the family symboly and 
# get the corresponding famuily name
for i in all_TempStr:

    if i.FamilyName.startswith("二次结构-U型"):
        u_shape_collec.append(i)
     
    elif i.FamilyName.startswith("二次结构-方钢管"):
        rhs_shape_collec.append(i)

    elif i.FamilyName.startswith("二次结构-角钢"):
        ang_shape_collec.append(i)


for famType in u_shape_collec:
    targetValue = famType.LookupParameter("采购规格")

    u_w = famType.LookupParameter("U型件W").AsValueString()
    u_t1 = famType.LookupParameter("U型件t1").AsValueString()
    u_h1 = famType.LookupParameter("U型件h1").AsValueString()

    try:
        u_h2 = famType.LookupParameter("U型件h2").AsValueString()
        new_value = "U {}x{}x{}x{}".format(u_w,u_h1,u_h2,u_t1)
        # print(new_value)
        t = Transaction(doc,"Assign value")
        t.Start()
        targetValue.Set(new_value)
        t.Commit()

    except:

        new_value = "U {}x{}x{}".format(u_w,u_h1,u_t1)
        # print(new_value)
        t = Transaction(doc,"Assign value")
        t.Start()
        targetValue.Set(new_value)
        t.Commit()


for famType in rhs_shape_collec:
    targetValue = famType.LookupParameter("采购规格")

    rhs_w = famType.LookupParameter("方钢管-宽").AsValueString()
    rhs_h = famType.LookupParameter("方钢管-高").AsValueString()
    
    rhs_t = famType.LookupParameter("方钢管-壁厚t1").AsValueString()
    new_value = "口 {}x{}x{}".format(rhs_w,rhs_h,rhs_t)
    # print(new_value)
    t = Transaction(doc,"Assign value")
    t.Start()
    targetValue.Set(new_value)
    t.Commit()

for famType in ang_shape_collec:
    targetValue = famType.LookupParameter("采购规格")

    ang_l1 = famType.LookupParameter("角钢_d1").AsValueString()
    ang_l2 = famType.LookupParameter("角钢_d2").AsValueString()
    
    ang_t = famType.LookupParameter("角钢_t").AsValueString()
    new_value = "L {}x{}x{}".format(ang_l1,ang_l2,ang_t)
    # print(new_value)
    t = Transaction(doc,"Assign value")
    t.Start()
    targetValue.Set(new_value)
    t.Commit()
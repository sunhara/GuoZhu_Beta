# -*- coding: utf-8 -*-
import clr

from pyrevit import forms, script
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import UnitTypeId

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Creating collector instance and collecting all the stiffeners from the model
all_TempStr = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TemporaryStructure).WhereElementIsNotElementType()
all_gague = []

for i in all_TempStr:

    matIds = i.GetMaterialIds(False)
    for matId in matIds:

        mat_name = doc.GetElement(matId).Name
        if mat_name =="轻钢":
            all_gague.append(i)
        else:
            pass



for i in all_gague:
    matIds = i.GetMaterialIds(False)
    
    for matId in matIds:

        mat_name = doc.GetElement(matId).Name

        if mat_name == "轻钢":

            mat_vol = i.GetMaterialVolume(matId)
            mat_vol_m3 = UnitUtils.ConvertFromInternalUnits(mat_vol,UnitTypeId.CubicMeters)
            
            targetPara = i.LookupParameter("轻钢Volume")

            t = Transaction(doc,"light steel gague volume")
            t.Start()
            targetPara.Set(mat_vol_m3)
            t.Commit()
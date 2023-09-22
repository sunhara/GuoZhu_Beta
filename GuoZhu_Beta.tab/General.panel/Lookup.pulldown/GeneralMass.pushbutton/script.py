# -*- coding: utf-8 -*-
import clr
from pyrevit import forms


from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument


#Getting the mass of the element
def GetMatMass(ele):
    #default total mass 0
    totalMass = 0

    #loop all material's id and material volume
    mat_ids = ele.GetMaterialIds(False)
    for id in mat_ids:
        mat_vol = ele.GetMaterialVolume(id)
        mat_vol_m3 = UnitUtils.ConvertFromInternalUnits(mat_vol,UnitTypeId.CubicMeters)
        
        #calculate mass of material
        matEle = doc.GetElement(id)
        mat_density = matEle.LookupParameter("材料密度 kg/m³").AsDouble()
        density_kgm = UnitUtils.ConvertFromInternalUnits(mat_density,UnitTypeId.KilogramsPerCubicMeter)
        mass = mat_vol_m3 * density_kgm
        
        totalMass = totalMass+mass

    return totalMass

model_selected = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]


#Initiate weight set to 0
totalweight = 0


for i in model_selected:

    # Check if the selected element is Group or famly instance
    if i.ToString() == "Autodesk.Revit.DB.Group":

        subElementIds = i.GetMemberIds()
        groupEle = [doc.GetElement(i) for i in subElementIds]

        for e in groupEle:
            mass = GetMatMass(e)
            totalweight = totalweight + mass

    else:
        mass = GetMatMass(i)
        totalweight = totalweight + mass

forms.alert('所选物体总质量：{} kg'.format(totalweight), exitscript=True)    
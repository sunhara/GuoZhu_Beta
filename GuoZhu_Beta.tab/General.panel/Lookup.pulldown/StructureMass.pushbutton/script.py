# -*- coding: utf-8 -*-
import clr
import json
import csv

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

model_selected = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]

totalweight = 0

for i in model_selected:

    # Check if the selected element is Group or famly instance
    if i.ToString() == "Autodesk.Revit.DB.Group":

        eles = i.GetMemberIds()

        for e in eles:
            element = doc.GetElement(e)
            vol = element.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
            vol_m3 = UnitUtils.ConvertFromInternalUnits(vol,UnitTypeId.CubicMeters)
            totalweight = totalweight+vol_m3*7890
    else:
        vol = i.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
        vol_m3 = UnitUtils.ConvertFromInternalUnits(vol,UnitTypeId.CubicMeters)
        totalweight = totalweight+vol_m3*7890

forms.alert('所选钢结构物体总质量：{} kg'.format(totalweight), exitscript=True)    
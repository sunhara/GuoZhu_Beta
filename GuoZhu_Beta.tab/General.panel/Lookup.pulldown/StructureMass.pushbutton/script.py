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

def SubCompon(famIns):
    
    global all_selected_elements

    subCompIds = famIns.GetSubComponentIds()

    if len(subCompIds) == 0:  
        all_selected_elements.append(famIns)
    else:
        all_selected_elements.append(famIns)
        for i in subCompIds:
            all_selected_elements.append(doc.GetElement(i))



# function calculate all element's mass     
def CalculateMass(element):

    vol = element.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
    vol_m3 = UnitUtils.ConvertFromInternalUnits(vol,UnitTypeId.CubicMeters)
    global totalweight
    totalweight = totalweight+vol_m3*7890


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument


model_selected = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]

totalweight = 0

all_selected_elements = []


for i in model_selected:

    # Check if the selected element is Group or famly instance
    if i.ToString() == "Autodesk.Revit.DB.Group":

        eles = i.GetMemberIds()
        
        for e in eles:
            element = doc.GetElement(e)
            SubCompon(element)

    else:
        
        SubCompon(i)
        

uniqueElements = list(set([i.Id for i in all_selected_elements]))


[CalculateMass(doc.GetElement(e)) for e in uniqueElements]
forms.alert('所选钢结构物体总质量：{} kg'.format(totalweight), exitscript=True)    
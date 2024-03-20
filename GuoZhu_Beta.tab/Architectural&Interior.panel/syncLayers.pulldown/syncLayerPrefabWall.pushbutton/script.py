# -*- coding: utf-8 -*-

from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

famSymbols_collec = []
elementNames = []

# Loop through the element IDs and 
# get the corresponding Revit element Name for each ID unique
for id in selection:

    element = doc.GetElement(id)
    if element.Name not in elementNames:
        famSymbols_collec.append(doc.GetElement(element.GetTypeId()))
        elementNames.append(element.Name)
    else:
        pass



for famType in famSymbols_collec:
    targetValue = famType.LookupParameter("构造做法")

    layer1_t = round(famType.LookupParameter("预制墙体_Layer1_t").AsDouble()*304.8,1)
    layer1 = famType.LookupParameter("墙体材质_Layer1").AsValueString()

    layer2_t = round(famType.LookupParameter("预制墙体_Layer2_t").AsDouble()*304.8,1)
    layer2 = famType.LookupParameter("墙体材质_Layer2").AsValueString()

    layer3_t = round(famType.LookupParameter("预制墙体_Layer3_t").AsDouble()*304.8,1)
    layer3 = famType.LookupParameter("墙体材质_Layer3").AsValueString()

    layer4_t = round(famType.LookupParameter("预制墙体_Layer4_t").AsDouble()*304.8,1)
    layer4 = famType.LookupParameter("墙体材质_Layer4").AsValueString()

    layer4_check = famType.LookupParameter("墙体_Layer4").AsValueString()

    line1 = str(layer1_t)+" "+layer1
    line2 = str(layer2_t)+" "+layer2
    line3 = str(layer3_t)+" "+layer3
    line4 = str(layer4_t)+" "+layer4

    #Assign text to multiple texts

    if layer4_check =="Yes":
        all_assembly = [line1,line2,line3,line4]
        multi_text = "\r\n".join(all_assembly)
        
        t = Transaction(doc,"Assign value")
        t.Start()
        targetValue.Set(multi_text)
        t.Commit()

    else:
        all_assembly = [line1,line2,line3]
        multi_text = "\r\n".join(all_assembly)
        
        t = Transaction(doc,"Assign value")
        t.Start()
        targetValue.Set(multi_text)
        t.Commit()
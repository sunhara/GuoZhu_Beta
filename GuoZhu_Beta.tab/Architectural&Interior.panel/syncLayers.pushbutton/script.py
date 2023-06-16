# -*- coding: utf-8 -*-
import clr
import json

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

#All walls
wallTypes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsElementType()
#All roofs
roofTypes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Roofs).WhereElementIsElementType()
#All Floors
floorTypes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsElementType()
#All Soffits
soffitTypes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RoofSoffit).WhereElementIsElementType()

#Turn into python lists
wt = [e for e in wallTypes]
rt = [e for e in roofTypes]
ft = [e for e in floorTypes]
st = [e for e in soffitTypes]
allAssemblys = wt+rt+ft+st

for aa in allAssemblys:
    if aa.GetCompoundStructure() != None:

        
        compound_structure = aa.GetCompoundStructure().GetLayers()
        #Get layers materials
        mat_ids = []
        mat_width = []
        for i in compound_structure:
            mat_ids.append(i.MaterialId)
            mat_width.append(round(i.Width*304.8))
        # Material's name    
        mat_name = [doc.GetElement(e).Name for e in mat_ids]

        mat_width_str = [str(e) for e in mat_width]
    
        #Assign text to multiple texts
        all_assembly = []
        for i,j in zip(mat_name,mat_width_str):
            all_assembly.append(j+" "+i)
        assembly_mulitx = "\r\n".join(all_assembly)

        targetValue = aa.LookupParameter("构造做法")
        # for exception
        if  not targetValue:
            pass
        else:
            t = Transaction(doc,"Assign value")
            t.Start()
            targetValue.Set(assembly_mulitx)
            t.Commit()
    
       


#print(assembly_mulitx)
# print("--"*50)
# print(json.dumps(wall_assembly1,encoding ='utf-8',ensure_ascii=False))
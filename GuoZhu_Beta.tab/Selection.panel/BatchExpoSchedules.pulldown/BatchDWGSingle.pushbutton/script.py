# -*- coding: utf-8 -*-
import json	
import clr
import math

from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = uidoc.Selection.GetElementIds()

# check for selection
if len(selection) == 0:
    forms.alert("请先高亮选择导出视图!")
    script.exit()
else:
    pass

views = []

target_folder = forms.pick_folder()

# check for directory
if target_folder == None:
    script.exit()
else:
    pass

option = DWGExportOptions()
# Loop through the element IDs and get the corresponding Revit element for each ID
for i in selection:

    element = doc.GetElement(i)
    name = element.Name
    views.append(name)

    icollectionID = List[ElementId]([i])
  
    doc.Export(target_folder,name,icollectionID,option)
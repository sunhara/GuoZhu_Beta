# -*- coding: utf-8 -*-
import json	
import os
import clr

from pyrevit import forms	
from pyrevit import script

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document

# Define the file path
file_path = os.environ['USERPROFILE'] + '\Desktop'

print('位置' + os.environ['USERPROFILE'] + '\Desktop')


selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

elements = []
ele_names = []
# Loop through the element IDs and get the corresponding Revit element for each ID
for id in selection:
    element = doc.GetElement(id)
    elements.append(element)


for e in elements:

    export_options = ViewScheduleExportOptions()
    export_options.FieldDelimiter = ","  # set the field delimiter to comma
    export_options.Title = True
    
    title = e.Name
    ele_names.append(title)

    e.Export(file_path, "{}.csv".format(title), export_options)





print("已导出清单：")
print(json.dumps(ele_names,encoding ='utf-8',ensure_ascii=False))


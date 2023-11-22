# -*- coding: utf-8 -*-

import sys
import clr
import uuid


from pyrevit import forms,script

output = script.get_output()

from Autodesk.Revit.DB import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_IDs = uidoc.Selection.GetElementIds()
GUID = uuid.uuid4()

#Check if the element has been selected
check = len(selected_IDs) == 0
if check:
    sys.exit()

t = Transaction(doc, 'Assign Marks')
t.Start()

for i in selected_IDs:
    ele = doc.GetElement(i)
    target = ele.LookupParameter("工厂加工-组装标号")
    target.Set(str(GUID))
  

t.Commit()
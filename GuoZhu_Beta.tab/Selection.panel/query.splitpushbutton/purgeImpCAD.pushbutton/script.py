# -*- coding: utf-8 -*-
import clr

import json

clr.AddReference('System')
from System.Collections.Generic import List


import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import forms,script


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

# Creating collector instance and collecting all the stiffeners from the model
collector = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()

for e in collector:

    print(e.Category.Name)
    print("链接--{}".format(e.IsLinked))
    try:
        viewname = doc.GetElement(e.OwnerViewId).Name
        print(viewname)

    except:
        pass


# print(json.dumps(elem.Name,encoding ='utf-8',ensure_ascii=False))
t = Transaction(doc, "purge")
t.Start()

for e in collector:
    if e.IsLinked == True:
        pass
    else:
        doc.Delete(e.Id)


t.Commit()

elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElementIds()

selected_ID = uidoc.Selection.GetElementIds()

selected_eles = [doc.GetElement(i).Name for i in selected_ID]


print("total elements")
print(len(elements))
print("selected types")
out1 = list(set(selected_eles))
print(len(out1))

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

ele = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]
type = [i.Name for i in ele]

uniqueList = list(set(type))
print(len(uniqueList))

print(len(elements))
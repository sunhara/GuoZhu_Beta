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





print(len(elements))
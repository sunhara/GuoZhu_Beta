# -*- coding: utf-8 -*-
import json	
import clr


from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*


doc = __revit__.ActiveUIDocument.Document

#Get the selected element
selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

model_groups = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType().ToElements()

#STAR THE TRANSACTION!!!
t = Transaction(doc, 'Isolate Elements')
t.Start()

# Get all members of the model group
assemblies = []

for m in model_groups:
    eles = m.GetMemberIds()
    #get assembly mark
    assembly_mark = m.LookupParameter("工厂加工-构件标号").AsString()
    if assembly_mark is not None:

        assemblies.append(assembly_mark)
        #apply 
        for e in eles:       
            element = doc.GetElement(e)
            elementMark = element.LookupParameter("工厂加工-构件标号")
            if elementMark is not None:
                elementMark.Set(assembly_mark)
            else:
                pass
    else:
        pass


t.Commit()

print(assemblies)
print(':OK_hand:',"DONE!")

#print(json.dumps(dataListRow,encoding ='utf-8',ensure_ascii=False))

# -*- coding: utf-8 -*-
import json	
import clr
import math

from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import ObjectType

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

currentView = uidoc.ActiveView

#Revti reference face to face & get edges

edge1 = uidoc.Selection.PickObject(ObjectType.Edge)

point1 = uidoc.Selection.PickPoint()
point2 = uidoc.Selection.PickPoint()

# face = uidoc.Selection.PickPoint()

#ref = uidoc.Selection.PickObjects(ObjectType.Face)

#face = doc.GetElement(face_ref).GetGeometryObjectFromReference(face_ref)

line = Line.CreateBound(point1,point2)


print(point2)




references = ReferenceArray
references.Append(edge1.GetEndPointReference(0))
references.Append(edge1.GetEndPointReference(1))

print(references)

doc.Create.NewDimension(currentView, edge1, references)

print(point1)
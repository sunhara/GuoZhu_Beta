# -*- coding: utf-8 -*-
import json	
import os
import clr
import csv 
import codecs

from pyrevit import forms	
from pyrevit import script
from operator import itemgetter, attrgetter, methodcaller
import Autodesk
from Autodesk.Revit.DB import*


doc = __revit__.ActiveUIDocument.Document
#Get the selected element
selection = __revit__.ActiveUIDocument.Selection.GetElementIds()
element = doc.GetElement(selection[0])

selection2 = __revit__.ActiveUIDocument.Selection.PickObject(Face)

#Revti element convert to Topo faces
geometry_options = Options()
geometry_options.ComputeReferences = True



face_ref = ElementReferenceType.REFERENCE_TYPE_SURFACE
face_ref2 = Reference(element)
geometry3 = element.GetGeometryObjectFromReference(face_ref2)




print(geometry3)

solid_options = SolidOptions(ElementId.InvalidElementId, ElementId.InvalidElementId)




# Get the geometry of the element

# Convert the geometry to a solid





     





#print(json.dumps(dataListRow,encoding ='utf-8',ensure_ascii=False))



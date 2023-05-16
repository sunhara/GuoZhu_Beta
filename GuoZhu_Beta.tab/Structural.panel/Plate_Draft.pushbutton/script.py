# -*- coding: utf-8 -*-
import json	
import os
import clr

from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import ObjectType

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


#Revti reference face to face& get edges
face_ref = uidoc.Selection.PickObject(ObjectType.Face)
face = doc.GetElement(face_ref).GetGeometryObjectFromReference(face_ref)
edges = face.EdgeLoops

#Get the selected element's mark from the face_ref
ele_id = face_ref.ElementId
ele_mark = doc.GetElement(ele_id).LookupParameter("工厂加工-零件标号").AsString()

if ele_mark is not None:

    #Start Transaction
    t = Transaction(doc, 'Create Plate Drawing')
    t.Start()


    #Create new Drafting view
    view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

    view_types_drafting = [vt for vt in view_types if vt.ViewFamily == ViewFamily.Drafting]
    view_type_drafting  = view_types_drafting[0]

    new_view = ViewDrafting.Create(doc,view_type_drafting.Id)
    new_view.Name= ele_mark


    curves = []

    for edge_loop in edges:
        for edge in edge_loop:

            curve = edge.AsCurve()
            curves.append(curve)

    for c in curves:

        detail_curve = doc.Create.NewDetailCurve(new_view, c)


    t.Commit()

else:
    forms.alert('需要零件标号', exitscript=True)


print(ele_mark)
print("-"*100)
print(curves)
print("-"*100)



#print(json.dumps(dataListRow,encoding ='utf-8',ensure_ascii=False))



# -*- coding: utf-8 -*-
import clr

from pyrevit import forms	

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = uidoc.ActiveView

groupEle_to_isolate = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]

#Resize the bounding box
if len(groupEle_to_isolate) !=0 :

    #STAR THE TRANSACTION!!!
    t = Transaction(doc, 'Isolate Elements')
    t.Start()

    # Get all members of the model group
    members = groupEle_to_isolate[0].GetMemberIds()


    #create bounding box and offset around element
    bbox = groupEle_to_isolate[0].get_BoundingBox(None)
    box_max = bbox.Max
    box_min = bbox.Min
    factor = 0.001
    new_box_max = box_max.Add(XYZ(factor,factor,factor))
    new_box_min = box_min.Add(XYZ(-factor,-factor,-factor))

    new_bbox = BoundingBoxXYZ()
    new_bbox.Max = new_box_max
    new_bbox.Min = new_box_min
    active_view.SetSectionBox(new_bbox)

    t.Commit()

else :
    forms.alert('需要选中模型组', exitscript=True)
# -*- coding: utf-8 -*-
import json	
import os
import clr

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms	
from pyrevit import script
output = script.get_output()

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import ObjectType

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_ID = uidoc.Selection.GetElementIds()

#Check if the copy element has been selected
check = len(selected_ID) != 0

if check == True:

    # Get the click points
    pt1 = uidoc.Selection.PickPoint()
    pt2 = uidoc.Selection.PickPoint()
 

    # Create a vector from the two points
    vector = XYZ(pt2.X - pt1.X, pt2.Y - pt1.Y, pt2.Z - pt1.Z)
   
    number_as_string = input("复制数量")
    number_of_copy = int(number_as_string)

    t = Transaction(doc, 'Copy Elements')
    t.Start()

    for i in range(1,number_of_copy+1):
        ElementTransformUtils.CopyElements(doc, selected_ID, i*vector)


    t.Commit()

    output.close()
else:
    forms.alert('需要先选择一个模型', exitscript=True)
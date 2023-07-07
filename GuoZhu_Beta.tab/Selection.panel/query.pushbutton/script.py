# -*- coding: utf-8 -*-
import clr
import json
import csv
import os

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

#Create the solid for matching
solids = []
selection = uidoc.Selection.GetElementIds()
print(selection)
solid_pt = XYZ

for i in selection:
    target = doc.GetElement(i)
    solid_pt = target.Location.Point

    option = Options()
    option.ComputeReferences = True
    option.DetailLevel = ViewDetailLevel.Fine
    geo_elem = target.Geometry[option]
    
    for obj in geo_elem:
        if isinstance(obj, Solid):
            if obj.Volume != 0:
                solids.append(obj)

#create result for segments
segments = []

cloud_vector = solid_pt-XYZ(0,0,0)
soliCur_option = SolidCurveIntersectionOptions()

pt2 = solid_pt.Add(XYZ(0,0,-0.01))

#line = doc.GetElement(ElementId(581139)).ChangeToReferenceLine()
line = Line.CreateBound(solid_pt, pt2)

for s in solids:
    result = s.IntersectWithCurve(line,soliCur_option)
    segments.append(result.SegmentCount)

print(segments)
in_pt = float(segments.count(0))
out_pt = float(len(segments))
percentage = (in_pt/out_pt)*100
print(percentage)
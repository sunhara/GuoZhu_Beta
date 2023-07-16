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
from Autodesk.Revit.DB import PointClouds
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

#ptCloud = doc.GetElement(uidoc.Selection.GetElementIds()[0])

#ptCloud = doc.GetElement(ElementId(579105))
ptCloud = doc.GetElement(ElementId(582289))

#Create filter
# Filter will match 1/1 of the overall point cloud
# Use the bounding box (filter coordinates are in the coordinates of the model)
boundingBox = ptCloud.get_BoundingBox(None)
planes = []
#midpoint = (boundingBox.Min + boundingBox.Max) / 2
midpoint = boundingBox.Max
# X boundaries
planes.append(Plane.CreateByNormalAndOrigin(XYZ.BasisX, boundingBox.Min))
planes.append(Plane.CreateByNormalAndOrigin(-XYZ.BasisX, midpoint))

# Y boundaries
planes.append(Plane.CreateByNormalAndOrigin(XYZ.BasisY, boundingBox.Min))
planes.append(Plane.CreateByNormalAndOrigin(-XYZ.BasisY, midpoint))

# Z boundaries
planes.append(Plane.CreateByNormalAndOrigin(XYZ.BasisZ, boundingBox.Min))
planes.append(Plane.CreateByNormalAndOrigin(-XYZ.BasisZ, midpoint))


# Create filter
filter = PointClouds.PointCloudFilterFactory.CreateMultiPlaneFilter(planes)
#parameters setting
averageDistance = 0.1
numberOfPoints= 1000

pts_collection = ptCloud.GetPoints(filter,averageDistance,numberOfPoints)
pts = [p for p in pts_collection]

pts_xyz =[]
for pt in pts:
    pt_xyz = XYZ(pt.X,pt.Y,pt.Z)
    pts_xyz.append(pt_xyz)
    
print(len(pts_xyz))


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#Create the solid for matching
solids = []
selection = uidoc.Selection.GetElementIds()
solid_pt = XYZ

for i in selection:
    target = doc.GetElement(i)
    print(target)
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

# Examine all points if its in the solid
for pt in pts_xyz:
    #print(pt.X,pt.Y,pt.Z)
    
    newPt = pt.Add(cloud_vector)
    pt2 = pt.Add(XYZ(0,0,0.01))

    line = Line.CreateBound(newPt, pt2)
    
    for s in solids:
        result = s.IntersectWithCurve(line,soliCur_option)
        segments.append(result.SegmentCount)


print("---"*50)
print(segments)
in_pt = float(segments.count(0))
out_pt = float(len(segments))
percentage = (in_pt/out_pt)*100
print(percentage)
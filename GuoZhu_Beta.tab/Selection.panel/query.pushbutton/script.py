# -*- coding: utf-8 -*-
import clr
clr.AddReference('System')
from System.Collections.Generic import List


from pyrevit import forms	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)


planes = []
#Current BoundingBox
bbox = active_view.CropBox
bbox_max = bbox.Max
bbox_min = bbox.Min
#boundariesX 
planes.append(Plane.CreateByNormalAndOrigin(XYZ.BasisX,bbox_min))
planes.append(Plane.CreateByNormalAndOrigin(-XYZ.BasisX,bbox_max))

#boundariesY 
planes.append(Plane.CreateByNormalAndOrigin(XYZ.BasisY,bbox_min))
planes.append(Plane.CreateByNormalAndOrigin(-XYZ.BasisY,bbox_max))

#boundariesZ 
planes.append(Plane.CreateByNormalAndOrigin(XYZ.BasisZ,bbox_min))
planes.append(Plane.CreateByNormalAndOrigin(-XYZ.BasisZ,bbox_max))

#List[Plane](planes)

point_cloud_instances = FilteredElementCollector(doc).OfClass(PointCloudInstance)
ptCloud = point_cloud_instances.FirstElement()

ptFilter = Autodesk.Revit.DB.PointClouds.PointCloudFilterFactory.CreateMultiPlaneFilter(planes)

pts = ptCloud.GetPoints(ptFilter,0.001,20)

elements = []

for point in pts:
    x = point.X
    y = point.Y
    z = point.Z
    xyz_point = XYZ(x, y, z)
    print(xyz_point)



scanName = ptCloud.GetScans()
sel_Filter = ptCloud.GetSelectionFilter()

print(ptCloud)

print("-"*50)
print(pts)
print(pts.Count)


print("-"*50)

# -*- coding: utf-8 -*-

import clr

from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import ObjectType

def GetWorkPlane(face):

    # Get the reference face
    
    planar_face = doc.GetElement(face).GetGeometryObjectFromReference(face)

    face_normal = planar_face.FaceNormal
    face_orig = planar_face.Origin

    newPlane = Plane.CreateByNormalAndOrigin(face_normal,face_orig)

    
    return newPlane

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

selected_ID = uidoc.Selection.GetElementIds()
#selected_ELE = doc.GetElement(selected_ID[0])
#Check if the copy element has been selected
check = len(selected_ID) != 0

t = Transaction(doc, 'Copy Elements')
t.Start()

# Get the first plane of the reference face
face_ref = uidoc.Selection.PickObject(ObjectType.Face)

nPlane = GetWorkPlane(face_ref)
view.SketchPlane = SketchPlane.Create(doc, nPlane)

# Create point1
pt1 = uidoc.Selection.PickPoint()

################################################################

# Get the second plane of the reference face
face_ref = uidoc.Selection.PickObject(ObjectType.Face)

nPlane = GetWorkPlane(face_ref)
view.SketchPlane = SketchPlane.Create(doc, nPlane)
pt2 = uidoc.Selection.PickPoint()

# Create a vector from the two points
vector = XYZ(pt2.X - pt1.X, pt2.Y - pt1.Y, pt2.Z - pt1.Z)

t.Commit()

print(nPlane)
print(vector)
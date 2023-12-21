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

#Revti reference face to face & get edges
face_ref = uidoc.Selection.PickObject(ObjectType.Face)
face = doc.GetElement(face_ref).GetGeometryObjectFromReference(face_ref)

#function selecte rotation edge
def rotaEdge(face):
    uvX = face.XVector
    uvY = face.YVector

    if uvX.Z == 1 or uvX.Z == -1:
        return uvY
    else:
        return uvX

#function selecte the rotation edge
def RotaEdgeGama(face):
    uvX = face.XVector
    uvY = face.YVector
    if round(math.degrees(uvX.AngleTo(XYZ(0, 0, 1)))) ==90:
        return uvX
    else:
        return uvY
    
def NoneRotaEdgeGama(face):
    uvX = face.XVector
    uvY = face.YVector
    if round( math.degrees(uvX.AngleTo(XYZ(0, 0, 1)))) == 90 :
        return uvY
    else:
        return uvX

#function selecte the smaller degrees
def chooseAng(axis):
    testAng1 = math.degrees(axis.AngleTo(XYZ(1, 0, 0)))
    testAng2 = math.degrees(axis.AngleTo(XYZ(0, 1, 0)))
    if testAng1 >= testAng2:
        return testAng2
    else:
        return testAng1

#Get the selected element's mark from the face_ref
ele_id = face_ref.ElementId
ele_mark = doc.GetElement(ele_id).LookupParameter("工厂加工-零件标号").AsString()


faceOrigin = face.Origin
faceNormal = face.ComputeNormal(UV(0.5,0.5))
ang = math.degrees(faceNormal.AngleTo(XYZ(0, 0, 1)))


curves = []

# print(ang)

if ang==0 or ang==180:
    curveLoops = face.GetEdgesAsCurveLoops()

    for loops in curveLoops:

        iterator = loops.GetCurveLoopIterator()
        while iterator.MoveNext():
            curves.append(iterator.Current)
    

elif ang == 90 or ang ==270:
    #Rotate on the XY plane

    axis = rotaEdge(face)

    curveLoops = face.GetEdgesAsCurveLoops()
    
    transform1 = Transform.CreateRotationAtPoint(axis, 90 * (math.pi / 180),faceOrigin)
    curveLoopsTrans1 = [CurveLoop.CreateViaTransform(c,transform1) for c in curveLoops]


    #Rotate on the YZ plane
    #select rotation degrees
    angBeta = chooseAng(axis)
    
    transform2 = Transform.CreateRotationAtPoint(XYZ(0,0,1), angBeta* (math.pi / 180),faceOrigin)
    curveLoopsTrans2 = [CurveLoop.CreateViaTransform(c,transform2) for c in curveLoopsTrans1]
    
    for loops in curveLoopsTrans2:

        iterator = loops.GetCurveLoopIterator()
        while iterator.MoveNext():
            curves.append(iterator.Current)
    
else:
      #Rotate on the XY plane


    uvX = face.XVector
    
    math.degrees(uvX.AngleTo(XYZ(0, 0, 1)))

    axis = RotaEdgeGama(face)
    noneAxis = NoneRotaEdgeGama(face)

    #Choosing the smaller degrees
    def choseAngeGama(axis):
        angG1 = math.degrees(axis.AngleTo(XYZ(0, 0, 1)))
        angG2 = math.degrees(axis.AngleTo(XYZ(0, 0, -1)))
        if angG1 >= angG2:
            return angG2
        else:
            return angG1
    choosenAng = choseAngeGama(noneAxis)

    curveLoops = face.GetEdgesAsCurveLoops()
    
    transform = Transform.CreateRotationAtPoint(axis, (90-choosenAng)* (math.pi / 180),faceOrigin)
    curveLoopsTrans = [CurveLoop.CreateViaTransform(c,transform) for c in curveLoops]


    #Rotate on the YZ plane
    #select rotation degrees
    def choseAngeGama2(axis):
        angG1 = math.degrees(axis.AngleTo(XYZ(0, 1, 0)))
        if angG1 <90:
            return angG1
        else:
            return (180-angG1)
            
    angGama = choseAngeGama2(axis)
    
    transform = Transform.CreateRotationAtPoint(XYZ(0,0,1), angGama* (math.pi / 180),faceOrigin)
    curveLoopsTrans = [CurveLoop.CreateViaTransform(c,transform) for c in curveLoopsTrans]

    for loops in curveLoopsTrans:

        iterator = loops.GetCurveLoopIterator()
        while iterator.MoveNext():
            curves.append(iterator.Current)
    


# print("-"*100)
# print(curveLoops[0].GetPlane().Normal)

# print("-"*100)
# print(curveLoopsTrans[0].GetPlane().Normal)
# print("-"*100)
# print("-"*100)

# #print(json.dumps(dataListRow,encoding ='utf-8',ensure_ascii=False))

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

    for c in curves:

        detail_curve = doc.Create.NewDetailCurve(new_view, c)


    t.Commit()

else:
    forms.alert('需要零件标号', exitscript=True)

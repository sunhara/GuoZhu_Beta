# -*- coding: utf-8 -*-
import clr
import sys
import math
from System.Collections.Generic import List
from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

class ElementToCopy(forms.TemplateListItem):
    
    @ property
    def name(self):
        
        return self.LookupParameter("Material").AsValueString()



#sellect elements and Collect all parts
t = Transaction(doc,"create tiles")
t.Start()

currView = doc.ActiveView 
parts_visual_setting = currView.LookupParameter("Parts Visibility")
# Parts Visibility setting 1 is origin 0 is parts only
parts_visual_setting.Set(1)
elementSelectionId = uidoc.Selection.PickObject(ObjectType.Element,"选择一个模型").ElementId

all_parts = PartUtils.GetAssociatedParts(doc, elementSelectionId, False, False)


# selecting the layers for split
parts_mat = [doc.GetElement(i) for i in all_parts]

options = [ElementToCopy(e) for e in parts_mat]

elesToCopy = forms.SelectFromList.show(options, title = "选择层", width = 500, button_name = "确定", multiselect = True)
ids = [i.Id for i in elesToCopy]
split_layers = List[ElementId](ids)


#detect the direction and return correct transform
def find_dir(vector,interval):
    return vector*interval


#pick the align lines
try:
    edge1 = uidoc.Selection.PickObject(ObjectType.Edge,"选择第1条对齐边")
    line1 = doc.GetElement(edge1).GetGeometryObjectFromReference(edge1).AsCurve()
    # print(line1.Origin)
    
    edge2 = uidoc.Selection.PickObject(ObjectType.Edge,"选择第2条对齐边")
    line2 = doc.GetElement(edge2).GetGeometryObjectFromReference(edge2).AsCurve()

    #detect the transform direction 
    refPoint = uidoc.Selection.PickObject(ObjectType.PointOnElement,"选择第内测点")
    pickPoint = refPoint.GlobalPoint
    
except:
    sys.exit()

l1_projectPoint = line1.Project(pickPoint).XYZPoint
l2_projectPoint = line2.Project(pickPoint).XYZPoint

line1Vector = (pickPoint - l1_projectPoint).Normalize()
line2Vector = (pickPoint - l2_projectPoint).Normalize()


#get the intersection point as origin
#Calculates the intersection of this curve with the specified curve 
#and returns the intersection results.

intersection_results = clr.Reference[IntersectionResultArray]()
result = line1.Intersect(line2,intersection_results)

#type mismatch; To avoid mistakenly treated as a subscriptable
interResult = intersection_results.Value
originP = interResult[0].XYZPoint

vector1 = (line1.GetEndPoint(1)-line1.GetEndPoint(0)).Normalize()
vector2 = (line2.GetEndPoint(1)-line2.GetEndPoint(0)).Normalize()
newPlane = Plane.CreateByOriginAndBasis(originP,vector2,vector1)


#define the tile's length and width
tileX = float(raw_input("输入分隔长"))
print("分隔长:{}".format(tileX))
tileY = float(raw_input("输入分隔宽"))
print("分隔宽:{}".format(tileY))

#calculate range of array
range1 = math.ceil((line2.Length*304.8)/tileX)
range2 = math.ceil((line1.Length*304.8)/tileY)
# print(range1,range2)

tileX_inch = round(tileX/304.8,3)
tileY_inch = round(tileY/304.8,3)

# curve line has to longer than the pick line
line1.MakeBound(-5,line1.Length+5)
line2.MakeBound(-5,line2.Length+5)


curveArray = []
#set the array for line1
for i in range(int(range1)):

    transform1  = Transform.CreateTranslation(find_dir(line1Vector,tileX_inch)*i)
    newline1 = line1.CreateTransformed(transform1)
    curveArray.append(newline1)

#set the array for line2
for i in range(int(range2)):

    transform2  = Transform.CreateTranslation(find_dir(line2Vector,tileY_inch)*i)
    newline2 = line2.CreateTransformed(transform2)
    curveArray.append(newline2)


sketchPlane = SketchPlane.Create(doc,newPlane)

intersectionElementIds = List[ElementId]()

#create parts, intersectionElement ids be empty
PartUtils.DivideParts(doc, split_layers,intersectionElementIds, curveArray, sketchPlane.Id )

parts_visual_setting.Set(0)
t.Commit()
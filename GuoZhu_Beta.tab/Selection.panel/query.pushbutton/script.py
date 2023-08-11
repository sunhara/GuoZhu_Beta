# -*- coding: utf-8 -*-
import clr
import json
import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import forms	
from pyrevit import script


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

currentview = doc.ActiveView

# Creating collector instance and collecting all the plates from the model
all_plates = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructConnectionPlates).WhereElementIsNotElementType()
all_connections = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructConnections).WhereElementIsNotElementType()

# print([i for i in all_plates])

#Create option for detail level, Using current view
#Otherwhis it will gets None/null
options = Options()
options.View = currentview
options.ComputeReferences = True

#function change points coordinate from feet to mm
def ConvertPt(pt):

    x = UnitUtils.ConvertFromInternalUnits(pt.X, UnitTypeId.Millimeters)
    y = UnitUtils.ConvertFromInternalUnits(pt.Y, UnitTypeId.Millimeters)
    z = UnitUtils.ConvertFromInternalUnits(pt.Z, UnitTypeId.Millimeters)
    #formate string
    output = format(x,".8f")[:8]+format(y,".8f")[:8]+format(z,".8f")[:8]
    return output

#Define the JSON file path
json_file_fp = "C:\\Users\\6321011\\Desktop\\JSON.txt"

f = open(json_file_fp, "r")
JSON = f.read()
json_file = json.loads(JSON)


for i in all_plates:
    
    plate = i.get_Geometry(options)

    maxPoint = plate.GetBoundingBox().Max
    minPoint = plate.GetBoundingBox().Min
    midPoint = (maxPoint+minPoint)/2

    #Convert point to key
    item_key = ConvertPt(midPoint)
 
    param = i.LookupParameter("工厂加工-构件标号")
    t = Transaction(doc,"update")
    t.Start()
    
    param.Set(json_file[item_key])

    t.Commit()


    
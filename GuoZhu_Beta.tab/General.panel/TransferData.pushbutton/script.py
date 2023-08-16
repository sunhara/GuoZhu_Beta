# -*- coding: utf-8 -*-
import clr
import json
import Autodesk
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import UnitTypeId

from pyrevit import forms	
from pyrevit import script


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

currentview = doc.ActiveView

# Creating collector instance and collecting all the plates from the model
all_plates = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructConnectionPlates).WhereElementIsNotElementType()
all_connections = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructConnections).WhereElementIsNotElementType()
all_framing = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType()
all_column = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType()

#function extract plates from structureConnectionHandler
def extractPlate (connections):
    extracted_elements = []
    handler =[i for i in connections]
    for i in handler:
        subelements = i.GetSubelements()
        for sub in subelements:
            if sub.Category.Name == "Plates":

                extracted_elements.append(sub)

            else:
                pass

    return extracted_elements

subElements = extractPlate(all_connections)

# function for getting parameters id with parameter's name
# Will return parameter id
def getParaWtName(subEle, name):
    
    paraIds = subEle.GetAllParameters()
    for id in paraIds:
        ele = doc.GetElement(id)

        if ele == None:
            pass
        elif ele.Name == name:
            return id
        else:
            pass


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
#json_file_fp = "C:\\Users\\6321011\\Desktop\\JSON.txt"
json_file_fp = forms.pick_file(file_ext='txt')

f = open(json_file_fp, "r")
JSON = f.read()
json_file = json.loads(JSON)

#collection for all elements
all_elements = []
for i in all_plates:
    all_elements.append(i)
for i in all_framing:
    all_elements.append(i)
for i in all_column:
    all_elements.append(i)

#all elements adding sub elements
all_elements.extend(subElements)

#input data to all elements
for i in all_elements:
    #check if the item is Subelements or not
    if isinstance(i,Autodesk.Revit.DB.Subelement):

        
        maxPoint = i.GetBoundingBox(currentview).Max
        minPoint = i.GetBoundingBox(currentview).Min
        midPoint = (maxPoint+minPoint)/2

        #Convert point to key
        item_key = ConvertPt(midPoint)

        paramId1 = getParaWtName(i,"工厂加工-构件标号")
        paramId2 = getParaWtName(i,"工厂加工-零件标号")

        strValue1 = StringParameterValue(json_file[item_key][0])
        strValue2 = StringParameterValue(json_file[item_key][1])
        
        try:
            #try to parse json
            json_file[item_key][0]
            t = Transaction(doc,"update")
            t.Start()

            i.SetParameterValue(paramId1,strValue1)
            i.SetParameterValue(paramId2,strValue2)

            t.Commit()
        except Exception as e:
            print(e)
        
    

    else:
        
        ele = i.get_Geometry(options)
        
        maxPoint = ele.GetBoundingBox().Max
        minPoint = ele.GetBoundingBox().Min
        midPoint = (maxPoint+minPoint)/2

        #Convert point to key
        item_key = ConvertPt(midPoint)

        # targt the parameters
        param1 = i.LookupParameter("工厂加工-构件标号")
        param2 = i.LookupParameter("工厂加工-零件标号")

        try:
            #try to parse json
            json_file[item_key][0]
            t = Transaction(doc,"update")
            t.Start()
            
            param1.Set(json_file[item_key][0])
            param2.Set(json_file[item_key][1])

            t.Commit()
        except Exception as e:
            print(e)
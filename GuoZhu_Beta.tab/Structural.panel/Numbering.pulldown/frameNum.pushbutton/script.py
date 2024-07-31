# -*- coding: utf-8 -*-
import json	
import itertools

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

import Autodesk

from pyrevit import forms

from Autodesk.Revit.DB import Options	
from Autodesk.Revit.DB import * #Loading Revit's API classes
from Autodesk.Revit.UI import * #Loading Revit's API UI classes  


app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

#Structural Framing Numbering

t = Transaction(doc,"Start a new Transaction")


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

# compare XYZ similarity
def prunePoint(plist):

    x = 0
    for i in plist:
        x=x+1

        if i.IsAlmostEqualTo(plist[x-1]):
            plist.pop(x-1)
        else:
            pass
    
    # print(plist)
    return plist


def findSolid(solids):
    temp = []
    for solid in solids:
        if solid.Edges.IsEmpty:
            pass
        else:
            temp.append(solid)
    return temp[0]


#define the parameters group
all_ele_name = []
all_ele_volume = []
all_ele_length = []
all_ele_matName = []
all_ele_holesDistance = []
all_ele_flipped = []


# Filterout all needed elements
all_FramStructure = FilteredElementCollector(doc)
all_FramStructure.OfCategory(BuiltInCategory.OST_StructuralFraming)
all_FramStructure.WhereElementIsNotElementType()
all_Ele = all_FramStructure.ToElements()


for i in all_Ele:
    
    #collect all volume
    vol = i.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
    value = str(round(vol,5))
    all_ele_volume.append(value)

    #collect all type name
    name = i.Name
    all_ele_name.append(name)

    #collect all length
    length = i.get_Parameter(BuiltInParameter.STRUCTURAL_FRAME_CUT_LENGTH).AsDouble()
    len_value = str(round(length,5))
    all_ele_length.append(len_value)

    #collect all material
    matIds = i.GetMaterialIds(False)
    try:
        matId = matIds[0].ToString()
        all_ele_matName.append(matId)
    #By Category material will not be no id
    except:
        all_ele_matName.append("000000")

    #collect hole's distance and if mirrored
    isBeenCut = i.HasModifiedGeometry()
    
    if isBeenCut is True:
        m_options =  Options()
        geoElement = i.get_Geometry(m_options)
        geoInstances = [geo_obj for geo_obj in geoElement if isinstance(geo_obj, Solid)]

        solid = findSolid(geoInstances)
    
        #extract edges from solid return arcs

        edges = [edge.AsCurve() for edge in solid.Edges if isinstance (edge.AsCurve(),Arc) ]
        arcCenters = [arc.Center for arc in edges]
        

        #purged list of points
        purgedPoints = prunePoint(arcCenters)

        #SS's location point
        try:
            locationPoint = i.Location.Point
        except:
            startP = i.Location.Curve.GetEndPoint(0)
            endP = i.Location.Curve.GetEndPoint(1)
            locationPoint = (startP+endP)/2
            

        unsortedDis = [p.DistanceTo(locationPoint) for p in purgedPoints]
        sortedDis = sorted(unsortedDis)
        sortedStrDis = [str(len)[:5] for len in sortedDis]
        strDis = ';'.join(sortedStrDis)

        all_ele_holesDistance.append(strDis)

    else:
        #no modified also be true append ""
        all_ele_holesDistance.append("")

    isFlipped = i.FacingFlipped
    if isFlipped is True and isBeenCut is True:
        all_ele_flipped.append("_Flipped_")
    else:
        all_ele_flipped.append("_NoneFlip_")

    
#construct a dicttionary for elements and values

values = []
for i,j,n,o,k,m in zip(all_ele_name, all_ele_volume, all_ele_length,all_ele_matName,all_ele_holesDistance,all_ele_flipped):
    para_value = str(i+j+n+o+k+m)
    values.append(para_value)
    
# for i in values:
#     print(i)
keys = all_Ele

#group elements by keys
dictionary = dict(zip(keys, values))

grouped_dict = {}
for key, value in dictionary.items():
    if value not in grouped_dict:
        grouped_dict[value] = []
    grouped_dict[value].append(key)


ele_grouped = grouped_dict.values()
outputNummber = []

t.Start()
#start numbering parts
num = 0
for group in ele_grouped:
    num +=1

    item = flatten_list(group)
    for i in item:
        target_para = i.LookupParameter("工厂加工-零件标号")
        target_para.Set("LJ-GL"+str(num))
    
    outputNummber.append("LJ-GL"+str(num))

           
t.Commit()

print(outputNummber)

#print (json.dumps(tuples,encoding ='utf-8',ensure_ascii=False))
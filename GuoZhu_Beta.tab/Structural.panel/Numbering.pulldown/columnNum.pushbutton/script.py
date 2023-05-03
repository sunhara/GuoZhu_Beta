# -*- coding: utf-8 -*-
import json	
import itertools

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

import Autodesk

from pyrevit import forms

	
from Autodesk.Revit.DB import * #Loading Revit's API classes
from Autodesk.Revit.UI import * #Loading Revit's API UI classes  


app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc,"Start a new Transaction")


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list


#define the parameters group
all_ele_name = []
all_ele_volume = []
all_ele_length = []


# Filterout all needed elements
all_ColStructure = FilteredElementCollector(doc)
all_ColStructure.OfCategory(BuiltInCategory.OST_StructuralColumns)
all_ColStructure.WhereElementIsNotElementType()
all_Ele = all_ColStructure.ToElements()




for i in all_Ele:
    
    #collect all volume
    vol = i.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
    value = str(round(vol,5))
    all_ele_volume.append(value)

    #collect all type name
    name = i.Name
    all_ele_name.append(name)

    #collect all length
    len = i.get_Parameter(BuiltInParameter.INSTANCE_LENGTH_PARAM).AsDouble()
    len_value = str(round(len,5))
    all_ele_length.append(len_value)

#construct a dicttionary for elements and values

values = []
for i,j,n in zip(all_ele_name, all_ele_volume, all_ele_length):
    para_value = str(i+j+n)
    values.append(para_value)
    
    
keys = all_Ele

dictionary = dict(zip(keys, values))

grouped_dict = {}
for key, value in dictionary.items():
    if value not in grouped_dict:
        grouped_dict[value] = []
    grouped_dict[value].append(key)


ele_grouped = grouped_dict.values()
test = []

t.Start()
#start numbering parts
num = 0
for group in ele_grouped:
    num +=1

    item = flatten_list(group)
    for i in item:
        target_para = i.LookupParameter("工厂加工-零件标号")
        target_para.Set("LJ-GZ"+str(num))
    
    test.append("LJ-GZ"+str(num))

           
t.Commit()


print(test)


#print (json.dumps(tuples,encoding ='utf-8',ensure_ascii=False))
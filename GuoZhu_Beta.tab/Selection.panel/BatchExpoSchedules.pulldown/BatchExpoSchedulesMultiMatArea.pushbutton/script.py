# -*- coding: utf-8 -*-
import json	
import os
import csv 
import codecs


from pyrevit import forms, script

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document

# Define the file path
file_path = os.environ['USERPROFILE'] + '\Desktop'


selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

elements = []

# Loop through the element IDs and get the corresponding Revit element for each ID
for id in selection:
    element = doc.GetElement(id)
    elements.append(element)

mat_dict = {}


for schedule in elements:
    table = schedule.GetTableData().GetSectionData(SectionType.Body)
    nRows = table.NumberOfRows
    

    #Iterator from the third index
    for row in range(2,nRows):

        mat_data = TableView.GetCellText(schedule, SectionType.Body, row, 1).splitlines()

        for matName in mat_data:

            #Convert to dict
            area = float(TableView.GetCellText(schedule, SectionType.Body, row, 2))
            dic_to_add = {matName:area}
            if matName in mat_dict.keys():
                newValue = mat_dict.get(matName) + area
                mat_dict.update({matName:newValue})
            else:
                mat_dict[matName] = area

#print(json.dumps(mat_dict,encoding ='utf-8',ensure_ascii=False))
    
try:
    titleName = forms.ask_for_string(default='材质面积总清单',prompt='清单命名:',title='清单命名')

    if titleName == None:
        script.exit()
except:
    script.exit()


field_names = ["材质", "面积㎡"] 
  
# In Python2.x use codecs for encoding & utf -8-sig for utf 8 with bom
with codecs.open('{}\\{}.csv'.format(file_path,titleName), mode = 'w', encoding ="utf-8-sig") as file:

    file.write("材质, 面积㎡\n")
    for key in mat_dict.keys():
        # "Hello %s, my name is %s" % ('john', 'mike') # Hello john, my name is mike".
            file.write("%s, %s\n" % (key, mat_dict[key]))
        

print("已导出清单：{}".format(titleName))
print('位置' + os.environ['USERPROFILE'] + '\Desktop')
#print(json.dumps(titles,encoding ='utf-8',ensure_ascii=False))
# -*- coding: utf-8 -*-
import json	
import os
import csv 
import codecs

from pyrevit import forms	
from pyrevit import script

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document

# Define the file path
file_path = os.environ['USERPROFILE'] + '\Desktop'

print('位置' + os.environ['USERPROFILE'] + '\Desktop')


selection = __revit__.ActiveUIDocument.Selection.GetElementIds()

elements = []
titles = []

# Loop through the element IDs and get the corresponding Revit element for each ID
for id in selection:
    element = doc.GetElement(id)
    elements.append(element)
    titles.append(element.Name) 

dataListRow = []

for schedule in elements:
    
    table = schedule.GetTableData().GetSectionData(SectionType.Body)
    nRows = table.NumberOfRows
    nColumns = table.NumberOfColumns

    dataListRow.Add([''])
    dataListRow.Add([''])
    #Collect all of data from the schedule
    
    for row in range(nRows): #Iterate through the rows. The second row is always a blank space
        dataListColumn = []
        for column in range(nColumns): #Iterate through the columns
            dataListColumn.Add( TableView.GetCellText(schedule, SectionType.Body, row, column) )
          
        dataListRow.Add( dataListColumn )



# In Python2.x use codecs for encoding & utf -8-sig for utf 8 with bom
with codecs.open('{}\\合并清单.csv'.format(file_path), mode = 'w', encoding ="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=",")
    
    for row in dataListRow:

        writer.writerow(row)
        

print("已导出清单：")
print(json.dumps(titles,encoding ='utf-8',ensure_ascii=False))
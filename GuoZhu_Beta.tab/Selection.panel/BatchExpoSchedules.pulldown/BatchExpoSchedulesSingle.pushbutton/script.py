# -*- coding: utf-8 -*-
import json	
import os
import clr
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

# Loop through the element IDs and get the corresponding Revit element for each ID
for id in selection:
    element = doc.GetElement(id)
    elements.append(element)


first_ele = elements[0]
restOf_ele = elements
restOf_ele.pop(0)


export_options = ViewScheduleExportOptions()
export_options.FieldDelimiter = ","  # set the field delimiter to comma
export_options.Title = True
    
first_ele.Export(file_path, "合并清单.csv", export_options)

dataListRow = []
for schedule in restOf_ele:
    
    table = schedule.GetTableData().GetSectionData(SectionType.Body)
    nRows = table.NumberOfRows
    nColumns = table.NumberOfColumns

    #Collect all of data from the schedule
    
    for row in range(nRows): #Iterate through the rows. The second row is always a blank space
        dataListColumn = []
        for column in range(nColumns): #Iterate through the columns
            dataListColumn.Add( TableView.GetCellText(schedule, SectionType.Body, row, column) )
          
        dataListRow.Add( dataListColumn )



# In Python2.x use codecs for encoding
with codecs.open('{}\\合并清单.csv'.format(file_path), mode = 'a', encoding ="utf-8") as file:
    writer = csv.writer(file, delimiter=",")
    
    for row in dataListRow:

        writer.writerow(row)
        




print(json.dumps(dataListRow,encoding ='utf-8',ensure_ascii=False))
print("已导出清单：")



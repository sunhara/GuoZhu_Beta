# -*- coding: utf-8 -*-
import clr
import json
import csv
import os

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

# Define the file path
file_path = os.environ['USERPROFILE'] + '\Desktop'
print('位置' + os.environ['USERPROFILE'] + '\Desktop')

#all the schedules in doc
schedules = FilteredElementCollector(doc).OfClass(ViewSchedule).ToElements()


schedu_on_sheet = []

#filter out the schedule on sheet
for s in schedules:
    sheet_id = s.OwnerViewId
    element = doc.GetElement(sheet_id)
    if element != None:
        if element.Name == active_view.Name:
            #the schedule's dependent sheet name = current sheet name
            schedu_on_sheet.append(s)

ele_names = []

#export schedules on sheet
for e in schedu_on_sheet:

    export_options = ViewScheduleExportOptions()
    export_options.FieldDelimiter = ","  # set the field delimiter to comma
    export_options.Title = True
    
    title = e.Name
    ele_names.append(title)

    e.Export(file_path, "{}.csv".format(title), export_options)

print("已导出清单：")
print(json.dumps(ele_names,encoding ='utf-8',ensure_ascii=False))


# -*- coding: utf-8 -*-
import clr
import json
import csv
import codecs

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

file_path = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\材料仓库-Adsklib\\材质密度.csv"


all_materials = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials).WhereElementIsNotElementType()

densLib = {}
# In Python2.x use codecs for encoding
with codecs.open(file_path, mode = 'r', encoding ="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for i in reader:
        densLib.update({i[0]:i[1]})
          

t = Transaction(doc,"set density")
t.Start()

for i in all_materials:
   # searching material density from library
    if densLib.get(i.Name) != None:
        density = float(densLib.get(i.Name))

        #Convert units
        density_kgm = UnitUtils.ConvertToInternalUnits(density,UnitTypeId.KilogramsPerCubicMeter)
        #target parameter
        mat_dens = i.LookupParameter("材料密度 kg/m³")

        mat_dens.Set(density_kgm)

t.Commit()

#print(json.dumps(row,encoding ='utf-8',ensure_ascii=False))
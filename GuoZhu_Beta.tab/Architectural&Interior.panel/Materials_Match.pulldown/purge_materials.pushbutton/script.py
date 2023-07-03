# -*- coding: utf-8 -*-
import clr
import json
import csv

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

doc_materials = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials).WhereElementIsNotElementType()
doc_matId = [e.Id for e in doc_materials]
mylist = List[ElementId](doc_matId)

res = forms.alert("所有材质将会被清理🗑!!!",ok = True)
if res:
    
    with Transaction(doc) as t:
        t.Start("delete materials")
        doc.Delete(mylist)

        t.Commit()
        TaskDialog.Show("Revit","材质已被清理🗑")
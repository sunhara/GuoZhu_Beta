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

collector = FilteredElementCollector(doc)
total = collector.GetElementCount()

print(total)
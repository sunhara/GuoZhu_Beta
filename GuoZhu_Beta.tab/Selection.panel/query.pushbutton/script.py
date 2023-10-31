# -*- coding: utf-8 -*-
import clr

clr.AddReference('System')
from System.Collections.Generic import List



import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import forms,script

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

# Creating collector instance and collecting all the stiffeners from the model
importIns = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()


output = script.get_output()

print([i.Category.Name for i in importIns])
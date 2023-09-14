# -*- coding: utf-8 -*-
import clr
import json

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import *

class ElementToCopy(forms.TemplateListItem):
    @property
    def name(self):
        return self.Name

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

# Define the source path 

file_path = forms.pick_file(file_ext='rfa')
fam_doc = app.OpenDocumentFile(file_path)

#Source family types
famTypes = [i for i in fam_doc.FamilyManager.Types]
famTypeNames = [i.Name for i in fam_doc.FamilyManager.Types]


options = [ElementToCopy(e) for e in famTypes]
elesToImport = forms.SelectFromList.show(options, title = "选择类型导入", width = 500, button_name = "导入", multiselect = True)
#Script exict point
if not elesToImport:
    fam_doc.Close(False)
    script.exit()

print(elesToImport)
t = Transaction(doc,"Copy Elements")
t.Start()

for i in elesToImport:
    doc.LoadFamilySymbol(file_path, i.Name)

t.Commit()

fam_doc.Close(False)
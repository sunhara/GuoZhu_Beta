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
file_path = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\材料仓库-Adsklib\\Materials Box\\Materials Library.rfa"
fam_doc = app.OpenDocumentFile(file_path)

#Source materials
materials = FilteredElementCollector(fam_doc).OfCategory(BuiltInCategory.OST_Materials).WhereElementIsNotElementType()
matNames = [e.Name for e in materials]

#Destination materials
doc_materials = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials).WhereElementIsNotElementType()
doc_matNames = [e.Name for e in doc_materials]

#filtering out the difference
x = set(doc_matNames)
y = set(matNames)
different = list(y.difference(x))

common_eles = []
for element in materials:
    if element.Name in different:
        common_eles.append(element)


options = [ElementToCopy(e) for e in common_eles]
elesToCopy = forms.SelectFromList.show(options, title = "选择材质导入", width = 500, button_name = "导入", multiselect = True)
#Script exict point
if not elesToCopy:
    fam_doc.Close(False)
    script.exit()


#Copy Element settings
ids = [e.Id for e in elesToCopy]
ids_copy= List[ElementId](ids)
copyOpts = CopyPasteOptions()
trans = Transform.Identity



t = Transaction(doc,"Copy Elements")
t.Start()

ElementTransformUtils.CopyElements(fam_doc,ids_copy,doc,trans,copyOpts)

t.Commit()

fam_doc.Close(False)

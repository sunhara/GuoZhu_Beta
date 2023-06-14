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
matIds = [e.Id for e in materials]

#Destination materials
doc_materials = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Materials).WhereElementIsNotElementType()
doc_matNames = [e.Name for e in doc_materials]
doc_matIds = [e.Id for e in doc_materials]

#filtering out the difference
x = set(doc_matNames)
y = set(matNames)
same = list(y.intersection(x))

common_eles = []
for element in materials:
    if element.Name in same:
        common_eles.append(element)


options = [ElementToCopy(e) for e in common_eles]
elesToCopy = forms.SelectFromList.show(options, title = "选择材质同步", width = 500, button_name = "同步", multiselect = True)
#Script exict point
if not elesToCopy:
    fam_doc.Close(False)
    script.exit()


#Copy Element settings
ids = [e.Id for e in elesToCopy]
ids_copy= List[ElementId](ids)
copyOpts = CopyPasteOptions()
trans = Transform.Identity


#filtering out the materials to delete
matNamesDel = [e.Name for e in elesToCopy]
xDel = set(matNamesDel)
yDel = set(matNames)
same = list(yDel.intersection(xDel))

dele_eles = []
for element in doc_materials:
    if element.Name in same:
        dele_eles.append(element)

#Delete Element 
ids_del = [e.Id for e in dele_eles]
ids_ToDel= List[ElementId](ids_del)

res = forms.alert("同步材质会移除当前材质，需要从新赋予材质！",ok = True)
if res:
    t = Transaction(doc,"Copy Elements")
    t.Start()

    doc.Delete(ids_ToDel) 

    ElementTransformUtils.CopyElements(fam_doc,ids_copy,doc,trans,copyOpts)

    t.Commit()

    fam_doc.Close(False)

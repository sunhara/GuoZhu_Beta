# -*- coding: utf-8 -*-
import clr
clr.AddReference('System')
clr.AddReference("System.Windows.Forms")

import sys

from System.Windows.Forms import  OpenFileDialog
from System.Collections.Generic import List
from Autodesk.Revit.DB import*

from pyrevit import script,forms

# class for selecting family symbol from their type names
class ElementToCopy(forms.TemplateListItem):
    @property
    def name(self):
        return self.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_ID = uidoc.Selection.GetElementIds()


#Check if the initial elements has been selected
if len(selected_ID) != 0:
    pass
else:
    script.exit()

# Collect all family symbol
allFamily = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsElementType().ToElements()

# Selection popup
options = [ElementToCopy(e) for e in allFamily]
famSymbol = forms.SelectFromList.show(options, title = "选择材质导入", width = 500, button_name = "导入", multiselect = True)


#Check if the copy elements has been selected
if famSymbol != None:
    pass
else:
    script.exit()



for i in selected_ID:
   

    element = doc.GetElement(i)

    location = element.Location

    hostface = element.HostFace

    startXYZ = element.Location.Point

    endXYZ = element.FacingOrientation

    t = Transaction(doc,"Start a new Transaction")
    t.Start()

    doc.Create.NewFamilyInstance(hostface,startXYZ,endXYZ,famSymbol[0])
     
    # doc.Create.NewFamilyInstance.Overloads[Reference, XYZ, XYZ, FamilySymbol](hostface,startXYZ,endXYZ,famSymbol[0])
     
    t.Commit() 
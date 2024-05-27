# -*- coding: utf-8 -*-
import clr
clr.AddReference('System')
clr.AddReference("System.Windows.Forms")

import sys

from System.Collections.Generic import List
from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import ObjectType


from pyrevit import script,forms

# class for selecting family symbol from their type names
class ElementToCopy(forms.TemplateListItem):
    @property
    def name(self):
        return self.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_ID = uidoc.Selection.GetElementIds()
selected_HostFace = uidoc.Selection.PickObject(ObjectType.Face,"选择host面")

#Check if the initial elements has been selected
if len(selected_ID) != 0:
    pass
else:
    script.exit()

# Collect all family symbol
allgeneric = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsElementType().ToElements()
allConnection = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructConnections).WhereElementIsElementType().ToElements()
combineFam = [i for i in allgeneric ] + [j for j in allConnection]

allFamily = List[Element](combineFam)


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

    startXYZ = element.Location.Point

    endXYZ = element.FacingOrientation

    t = Transaction(doc,"Start a new Transaction")
    t.Start()

    newVoids = doc.Create.NewFamilyInstance(selected_HostFace,startXYZ,endXYZ,famSymbol[0])

     
    # doc.Create.NewFamilyInstance.Overloads[Reference, XYZ, XYZ, FamilySymbol](hostface,startXYZ,endXYZ,famSymbol[0])
     
    t.Commit() 
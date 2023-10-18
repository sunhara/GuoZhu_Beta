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


def SubCompon(famIns):
    
    subCompIds = famIns.GetSubComponentIds()
    if len(subCompIds) == 0:
        return famIns
    else:
        return [doc.GetElement(i) for i in subCompIds]

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_ID = uidoc.Selection.GetElementIds()

famInstance = doc.GetElement(selected_ID[0])

obj = famInstance.GetMemberIds()

print(obj)
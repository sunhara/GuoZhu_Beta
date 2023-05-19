# -*- coding: utf-8 -*-
import clr

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms	
from pyrevit import script


from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


#Create the filter condition
class SteelPlateFilter(ISelectionFilter):
    def AllowElement(self, element):
        if element.ToString() == "Autodesk.Revit.DB.Steel.SteelProxyElement":
            return True
        else:
            return False



#Set the filtered elements to current selection
try:
    myfilter = SteelPlateFilter()
    filter_selection = uidoc.Selection.PickElementsByRectangle(myfilter)

    filtered_list = []
    for el in filter_selection:
        filtered_list.append(el.Id)

    filtered_element_ids = List [ElementId] ([element for element in filtered_list])
    uidoc.Selection.SetElementIds(filtered_element_ids)
except Exception:
    pass

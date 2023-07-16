# -*- coding: utf-8 -*-
import clr
clr.AddReference('System')
from System.Collections.Generic import List

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*

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
    
    filtered_element_ids = List [ElementId] ([element.Id for element in filter_selection])
    
    uidoc.Selection.SetElementIds(filtered_element_ids)
    
except Exception:
    pass
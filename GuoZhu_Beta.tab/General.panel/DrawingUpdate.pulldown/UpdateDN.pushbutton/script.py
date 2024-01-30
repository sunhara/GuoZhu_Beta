# -*- coding: utf-8 -*-
import json	
import clr

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms	
from pyrevit import script

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = uidoc.ActiveView


#Function to hide the untarget elements in the given View.
# def hide_elements(element,corrsId):

#     hide_elem = FilteredElementCollector(doc, view.Id).Excluding(elements).WhereElementIsNotElementType().ToElements()

#     hide_elem_ids = [e.Id for e in hide_elem 
#                       if e.CanBeHidden(view)]

#     view.HideElements(List[ElementId](hide_elem_ids))


selection = uidoc.Selection.GetElementIds()

view3Ds = []
ele_names = []


# Define the categories
strFram_cate = BuiltInCategory.OST_StructuralFraming
strCol_cate = BuiltInCategory.OST_StructuralColumns
plate_cate = BuiltInCategory.OST_StructuralStiffener
connec_cate = BuiltInCategory.OST_StructConnections
generic_cate = BuiltInCategory.OST_GenericModel
temporary_cate = BuiltInCategory.OST_TemporaryStructure

# Create a list of category filters
category_filters = []
category_filters.append(ElementCategoryFilter(strFram_cate))
category_filters.append(ElementCategoryFilter(strCol_cate))
category_filters.append(ElementCategoryFilter(plate_cate))
category_filters.append(ElementCategoryFilter(strCol_cate))
category_filters.append(ElementCategoryFilter(connec_cate))
category_filters.append(ElementCategoryFilter(generic_cate))
category_filters.append(ElementCategoryFilter(temporary_cate))

# Create a logical OR filter
logical_cate_filter = LogicalOrFilter(category_filters)


# Loop through the element IDs and get the corresponding Revit element for each ID
for id in selection:
    
    viewEles = FilteredElementCollector(doc, id).WherePasses(logical_cate_filter).WhereElementIsNotElementType().ToElements()
    
    



print(view3Ds)

# #input view name
# value = forms.ask_for_string(
        
#         prompt='输入视图名称:',
#         title='View Title Input'
#     )


# try:

#     elements_to_isolate = [doc.GetElement(e_id) 
#             for e_id in uidoc.Selection.GetElementIds()]

#     part_mark = elements_to_isolate[0].LookupParameter("工厂加工-零件标号").AsString()

#     if part_mark is not None and len(part_mark) != 0:

#         #STAR THE TRANSACTION!!!
#         t = Transaction(doc, 'Isolate Elements')
#         t.Start()

#         List_isolate_ids = uidoc.Selection.GetElementIds()

#         #Created new view with name
#         new_viewId = active_view.Duplicate(ViewDuplicateOption.Duplicate)
#         new_view_ele = doc.GetElement(new_viewId)
#         name = new_view_ele.get_Parameter(BuiltInParameter.VIEW_NAME)

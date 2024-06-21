# -*- coding: utf-8 -*-
import clr

from pyrevit import forms, script
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import UnitTypeId

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# allViews = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType()

selected_views  = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]



# t = Transaction(doc,"rename")
# t.Start()


for i in selected_views:
    viewName = i.LookupParameter("View Name")

    # i.GetDependentElements()
    elements = FilteredElementCollector(doc, i.Id)
    viewGuid = i.LookupParameter("视口关联GUID").AsString()

    #the elements in the view
    
    print(elements)
    for i in elements:
        print(i.Name)
        print(i.Category.Name)

        
    # for j in elements:

    #     try:
    #         eleGuid = j.LookupParameter("视口关联GUID").AsString()
    #         partMark = j.LookupParameter("工厂加工-零件标号").AsString()
            
    #         if viewGuid == eleGuid:

    #             viewName.Set(partMark)

    #     except:
    #         pass


# if value == None:
#     script.exit()


# t.Commit()
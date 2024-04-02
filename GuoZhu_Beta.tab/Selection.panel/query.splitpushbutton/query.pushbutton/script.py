# -*- coding: utf-8 -*-

from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = __revit__.ActiveUIDocument.Selection.GetElementIds()


# Creating collector collecting all the categories
all_categories = doc.Settings.Categories

model_cate = []
for i in all_categories:
    if i.CategoryType == CategoryType.Model:
        model_cate.append(i)

# modify category's and sub cate's  line weight
with Transaction(doc, "change line weights") as t:

    t.Start()
    for i in model_cate:
        # print(i.Name,i.CategoryType)
        i.SetLineWeight(1,GraphicsStyleType.Projection)
        sub_cate = i.SubCategories
        for sub in sub_cate:
            sub.SetLineWeight(1,GraphicsStyleType.Projection)

    t.Commit()

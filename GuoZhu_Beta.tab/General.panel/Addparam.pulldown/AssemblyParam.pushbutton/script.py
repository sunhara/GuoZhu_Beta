# -*- coding: utf-8 -*-
import clr
import json

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

#Set up the param categories
wall_cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Walls)
roof_cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Roofs)
soffit_cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_RoofSoffit)
floor_cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Floors)
#Add category to CatSets
catSet = doc.Application.Create.NewCategorySet()
catSet.Insert(wall_cat)
catSet.Insert(roof_cat)
catSet.Insert(soffit_cat)
catSet.Insert(floor_cat)


# Define the shared parameter file path
shared_para_fp = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\共享参数模板（Shared Parameters）\\Shared Parameters-2023.txt"

# Create a new shared parameter file object
spFile = doc.Application.OpenSharedParameterFile()
defGroups = spFile.Groups

groupNames = []
for dg in defGroups:
    groupNames.append(dg.Name)
    if dg.Name == "通用":
        
        exterianl_def = [d for d in dg.Definitions]

        for d in exterianl_def:
            if d.Name == "构造做法":

                with Transaction(doc) as t:    
                    t.Start("Add Shared Parameters")
                    #Binding the parameter to category 
                    newIB = doc.Application.Create.NewTypeBinding(catSet)
                    #Binding map insert
                    doc.ParameterBindings.Insert(d,newIB,BuiltInParameterGroup.PG_TEXT)
                    t.Commit()


  

# print(catSet)
# print("--"*50)
# print(json.dumps(groupNames,encoding ='utf-8',ensure_ascii=False))
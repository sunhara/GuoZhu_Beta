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


mat_cate = Category.GetCategory(doc,BuiltInCategory.OST_Materials)

cateSet = doc.Application.Create.NewCategorySet()
cateSet.Insert(mat_cate)


#Define the shared parameter file path
shared_para_fp = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\共享参数模板（Shared Parameters）\\Shared Parameters-2023.txt"

#Create a new shared parameter file object
app.SharedParametersFilename = shared_para_fp
spFile = doc.Application.OpenSharedParameterFile()
defGroups = spFile.Groups

groupNames = []
for dg in defGroups:
    groupNames.append(dg.Name)
    if dg.Name == "材料":
        
        exterianl_def = [d for d in dg.Definitions]

        for d in exterianl_def:
            if d.Name == "材料密度 kg/m³":
                
                with Transaction(doc) as t:    
                    t.Start("Add Shared Parameters")
                    #Binding the parameter to category 
                    newIB = doc.Application.Create.NewInstanceBinding(cateSet)
                    #Binding map insert
                    doc.ParameterBindings.Insert(d,newIB,BuiltInParameterGroup.PG_IDENTITY_DATA)

                    #Convert Externaldefinition to internalDefinition in order to SetAllowVaryBetweenGroups!
                    internal_sp = SharedParameterElement.Lookup( doc,d.GUID)
                    internal_sp.GetDefinition().SetAllowVaryBetweenGroups(doc,True)
                    t.Commit()


# print(catSet)
# print("--"*50)
# print(json.dumps(groupNames,encoding ='utf-8',ensure_ascii=False))
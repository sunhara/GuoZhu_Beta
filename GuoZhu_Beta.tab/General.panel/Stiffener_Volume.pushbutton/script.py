# dependencies
# -*- coding: utf-8 -*-
import clr
import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

# Creating collector instance and collecting all the stiffeners from the model
all_stiffeners = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralStiffener).WhereElementIsNotElementType()

#Stiffener category
stiff_cate = Category.GetCategory(doc,BuiltInCategory.OST_StructuralStiffener)
cateSet = doc.Application.Create.NewCategorySet()
cateSet.Insert(stiff_cate)

#Define the shared parameter file path
shared_para_fp = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\共享参数模板（Shared Parameters）\\Shared Parameters-2023.txt"

#Set the Condition
condition = all_stiffeners.ToElements()[0].LookupParameter("Stiffener_Volume")

Para = []

# Condition for whether it needs for adding a shared parameters
if condition == None or condition.IsReadOnly:

    #Create a new shared parameter file object
    app.SharedParametersFilename = shared_para_fp
    spFile = doc.Application.OpenSharedParameterFile()
    defGroups = spFile.Groups

    for dg in defGroups:
    #groupNames.append(dg.Name)

        if dg.Name == "钢板-Stiffener":
            
            exterianl_def = [d for d in dg.Definitions]

            for d in exterianl_def:
                if d.Name == "Stiffener_Volume":
                    
                    with Transaction(doc) as t:    
                        t.Start("Add Shared Parameters and set value")
                        #Binding the parameter to category 
                        newIB = doc.Application.Create.NewInstanceBinding(cateSet)
                        #Binding map insert
                        doc.ParameterBindings.Insert(d,newIB,BuiltInParameterGroup.PG_ANALYSIS_RESULTS)

                        #Convert Externaldefinition to internalDefinition in order to SetAllowVaryBetweenGroups!
                        internal_sp = SharedParameterElement.Lookup( doc,d.GUID)
                        internal_sp.GetDefinition().SetAllowVaryBetweenGroups(doc,True)

                        for i in all_stiffeners:
                            targetVolume = i.LookupParameter("Stiffener_Volume")
                            #compute family instance volume
                            volume = i.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED)
                            value = round(volume.AsDouble(),5)
                            Para.append(value)
                            #set to the variable
                            targetVolume.Set(value)

                        t.Commit()
else:
    t = Transaction(doc,"This is a new transaction")

    t.Start()
    for i in all_stiffeners:
        targetVolume = i.LookupParameter("Stiffener_Volume")
        #compute family instance volume
        volume = i.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED)
        value = round(volume.AsDouble(),5)
        Para.append(value)
        #set to the variable
        targetVolume.Set(value)

    t.Commit()

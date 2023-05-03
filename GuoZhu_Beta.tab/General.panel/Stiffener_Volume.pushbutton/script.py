# dependencies
# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document


# Creating collector instance and collecting all the stiffeners from the model
all_stiffeners = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralStiffener).WhereElementIsNotElementType()

t = Transaction(doc,"This is a new transaction")


Para = []


t.Start()


for i in all_stiffeners:
    targetVolume = i.LookupParameter("Stiffener_Volume")

    if  doc.Application.Language.ToString() == 'English_USA':
        #Or using Autodesk.Revit.ApplicationServices.LanguageType.English_USA
        volume = i.LookupParameter("Volume")
        value = round(volume.AsDouble(),5)
        Para.append(value)

        targetVolume.Set(value)

    else:
        volume = i.LookupParameter("体积")
        value = round(volume.AsDouble(),5)
        Para.append(value)
    
        targetVolume.Set(value)



t.Commit()

print(Para)


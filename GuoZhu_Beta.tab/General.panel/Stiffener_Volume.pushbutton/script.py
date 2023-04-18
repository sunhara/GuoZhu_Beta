# dependencies
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document


# Creating collector instance and collecting all the walls from the model
all_stiffeners = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralStiffener).WhereElementIsNotElementType()

t = Transaction(doc,"This is a new transaction")


Para = []


t.Start()


for i in all_stiffeners:
    targetVolume = i.LookupParameter("Stiffener_Volume")
    volume = i.LookupParameter("Volume")
    value = round(volume.AsDouble(),5)
    Para.append(value)
    
    targetVolume.Set(value)




t.Commit()

print(Para)


# -*- coding: utf-8 -*-
import clr
from pyrevit import forms
from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc =__revit__.ActiveUIDocument


current_matMass = []
#Getting the mass of the element
def GetMatMass(ele):
    #default total mass 0
    totalMass = 0


    #loop all material's id and material volume
    mat_ids = ele.GetMaterialIds(False)
    for id in mat_ids:
        mat_vol = ele.GetMaterialVolume(id)
        mat_vol_m3 = UnitUtils.ConvertFromInternalUnits(mat_vol,UnitTypeId.CubicMeters)
        
        #calculate mass of material
        matEle = doc.GetElement(id)
        mat_density = matEle.LookupParameter("材料密度 kg/m³").AsDouble()
        density_kgm = UnitUtils.ConvertFromInternalUnits(mat_density,UnitTypeId.KilogramsPerCubicMeter)
        mass = mat_vol_m3 * density_kgm
        # print(matEle.Name,mass)
        
        
        current_matMass.append([matEle.Name,mass])

        totalMass = totalMass+mass

    return totalMass


model_selected = [doc.GetElement(e_id) for e_id in uidoc.Selection.GetElementIds()]

famInstances = []
collect_elements = []


#Convert all selected group to revit DB ids
for i in model_selected:

    # Check if the selected element is Group 
    try:
        groMemberIds = i.GetMemberIds()
        for j in groMemberIds:
            famInstances.append(doc.GetElement(j))
    except:
        famInstances.append(i)

#extract all sub components from fam instance 
for i in famInstances:

    # Check if the selected element has Sub Components
    collect_elements.append(i)
    try:
        subElemen = i.GetSubComponentIds()
        for j in subElemen:
            collect_elements.append(doc.GetElement(j))
    except:
        pass


# print(collect_elements)

for i in collect_elements:
    GetMatMass(i)



values = set(map(lambda x: x[0],current_matMass))
newlist = [[y[1] for y in current_matMass if y[0]==x] for x in values]

mass_list = [sum(i) for i in newlist]

totalweight = sum(mass_list)


for i,j in zip(values,mass_list):
    print("{}---{}kg".format(i,j))
print("==="*20)
print('所选物体总质量：{} kg'.format(totalweight))
print("❗❗❗当材质质量为0，未赋予材质❗❗❗")



# forms.alert('所选物体总质量：{} kg'.format(totalweight), exitscript=True)    
# -*- coding: utf-8 -*-
import clr
import codecs

from pyrevit import forms, script
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import UnitTypeId

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selected_ID = uidoc.Selection.GetElementIds()

if len(selected_ID) ==0:
    forms.alert("先选择一个模型组", exitscript=True)
else:
    pass


selectedGroup  = doc.GetElement(selected_ID[0])

#The origin name of the group
groOriginName = selectedGroup.Name
#input view name

value = forms.ask_for_string(
        default = '{}'.format(groOriginName),
        prompt='输入新模型组名称，当前名称：: {}'.format(groOriginName),
        title='View Title Input'
    )

if value == None:
    script.exit()


t = Transaction(doc,"create group")
t.Start()

# selectedGroup.GroupType.Duplicate(value)

newMembers = selectedGroup.UngroupMembers()

newgroup = doc.Create.NewGroup(newMembers)
newgroup.GroupType.Name = value


t.Commit()
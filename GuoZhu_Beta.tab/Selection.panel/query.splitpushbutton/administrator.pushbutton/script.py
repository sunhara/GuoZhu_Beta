# -*- coding: utf-8 -*-
import clr
import xml.etree.ElementTree as ET

clr.AddReference('System')
from System.Collections.Generic import List
from Autodesk.Revit.UI import*

import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import forms,script


doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

app_username = app.Username



# xmal_file = script.get_bundle_file("ui.xaml")
# xmal_file = "C:\\Users\\6321011\\Desktop\\firstWPFApp\\firstWPFApp\\firstWPFApp\\ui.xaml"

#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"

XML_user_names = []
tree = ET.parse(public_config)
root = tree.getroot()

target_user = []
for user in root.findall("user"):

    if user.get("name") == app_username:
        target_user.append(user)


try: 

    if target_user[0].find("workset").text=="True":
        print("true")
    else:
        print("false1")
    
except:
    print("false2")

for i in root:
    value = i.attrib['name']
    # Input context with utf-8 must decode with utf-8
    XML_user_names.append(value.decode("utf-8"))

print(app_username)


























# The main code
# try:
#     value = forms.ask_for_string(
        
#         prompt='INPUT ADMIN CODE:',
#         title='Admin Check'
#     )

#     print(value)
#     if value == "1q2w3e4r":
#         print("correct")
#     else:
#         forms.alert("错误，请联系管理员")
# except:
#     script.exit()



# print(json.dumps(elem.Name,encoding ='utf-8',ensure_ascii=False))
# t = Transaction(doc, "purge")
# t.Start()

# for e in collector:
#     if e.IsLinked == True:
#         pass
#     else:
#         doc.Delete(e.Id)


# t.Commit()

# elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElementIds()

# selected_ID = uidoc.Selection.GetElementIds()

# selected_eles = [doc.GetElement(i).Name for i in selected_ID]


# print("total elements")
# print(len(elements))
# print("selected types")
# out1 = list(set(selected_eles))
# print(len(out1))


# CmndID = RevitCommandId.LookupCommandId('ID_SETTINGS_PARTITIONS')
# postCmndID = RevitCommandId.LookupPostableCommandId(PostableCommand.Worksets)
# print(postCmndID)
# CmId = CmndID.Id
# uiapp.PostCommand(postCmndID)
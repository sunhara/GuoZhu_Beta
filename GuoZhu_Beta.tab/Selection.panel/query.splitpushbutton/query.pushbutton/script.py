# -*- coding: utf-8 -*-
import clr
import xml.etree.ElementTree as ET
import os
import shutil
import json


from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


current_username = __revit__.Application.Username
#User input
# username = os.environ.get('USERNAME')


#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"
text_XML = "C:\\Users\\6321011\\Desktop\\textXML.xml"


# parse the public config(original) from the utf-8 xml
tree = ET.parse(public_config)
root = tree.getroot()



newRoot = ET.Element("data")

for rt in root:

    user = rt.get("name").decode("utf-8")
    print(user)
    admin = rt.find("admin").text
    print(admin)
    workset = rt.find("workset").text
    print(workset)

    newElem = ET.Element("user", name = user)

    subE1 = ET.SubElement(newElem, "admin")
    subE1.text = admin
    subE2 = ET.SubElement(newElem, "workset")
    subE2.text = workset

    # root.append(newElem)
    newRoot.append(newElem)

newTree = ET.ElementTree(newRoot)
newTree.write(text_XML, encoding="UTF-8",xml_declaration=True)

# -*- coding: utf-8 -*-
import clr
import xml.etree.ElementTree as ET


from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def tunning(newRoot):
    print("****"*10)
    for rt in newRoot:
        user = rt.get("name")
        print("<{}>".format(user))
        admin = rt.find("admin").text
        print("\t admin-{}".format(admin))
        workset = rt.find("workset").text
        print("\t workset-{}".format(workset))


output = script.get_output()

#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"
text_XML = "C:\\Users\\6321011\\Desktop\\textXML.xml"


app = __revit__.Application
app_username = app.Username

tree = ET.parse(public_config)
root = tree.getroot()

target_user = []
test = root.findall("user").get("name").decode("utf-8") == app_username

print(test)
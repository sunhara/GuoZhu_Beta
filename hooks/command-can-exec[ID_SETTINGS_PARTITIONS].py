# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from pyrevit import HOST_APP, EXEC_PARAMS


#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"

args = EXEC_PARAMS.event_args

app = __revit__.Application
app_username = app.Username

tree = ET.parse(public_config)
root = tree.getroot()

target_user = []
for user in root.findall("user"):

    if user.get("name") == app_username:
        target_user.append(user)


try: 

    if target_user[0].find("workset").text=="True":
        args.CanExecute = True
    else:
        args.CanExecute = False
    
except:
    args.CanExecute = False
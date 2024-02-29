#! python3

import xml.etree.cElementTree as ET
import os

from pyrevit import HOST_APP, EXEC_PARAMS

username = os.environ.get('USERNAME')

# local config

local_config = "C:\\Users\\{}\\AppData\\Roaming\\pyRevit\\GUOZHU_Beta_local_config.xml".format(username)

arg = EXEC_PARAMS
args = EXEC_PARAMS.event_args
print(arg)
app = __revit__.Application
app_username = app.Username


tree = ET.parse(local_config)
root = tree.getroot()

print(args)


target_user = []
for user in root.findall("user"):

    # print(user.get("name"))
    if user.get("name") == app_username:
        target_user.append(user)


try: 

    if target_user[0].find("workset").text=="True":
        
        args.CanExecute = True

        root.clear()
        

    else:
        args.CanExecute = False

        root.clear()      


except:
    args.CanExecute = False

    root.clear()
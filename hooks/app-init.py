# -*- coding: utf-8 -*-
import os
import shutil
import filecmp

from pyrevit import EXEC_PARAMS

args = EXEC_PARAMS.event_args

#User input
username = os.environ.get('USERNAME')

#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"
local_config = "C:\\Users\\{}\\AppData\\Roaming\\pyRevit\\GUOZHU_Beta_local_config.xml".format(username)


# Check if local config exist
if os.path.exists(local_config):


    # compare two file difference
    if filecmp.cmp(public_config,local_config):
        pass
    else:

        shutil.copyfile(public_config,local_config)
else:
    shutil.copyfile(public_config,local_config)
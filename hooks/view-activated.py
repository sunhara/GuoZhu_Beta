# -*- coding: utf-8 -*-
import clr
import codecs
import os
import shutil
import filecmp


from pyrevit import EXEC_PARAMS
from pyrevit import forms,script

args = EXEC_PARAMS.event_args

#User input
username = os.environ.get('USERNAME')

mess_log = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\worklog\\message_log.txt"
local_log = "C:\\Users\\{}\\AppData\\Roaming\\pyRevit\\local_message_log.txt".format(username)

# Check if local log exist
if os.path.exists(local_log):


    # compare two file difference
    if filecmp.cmp(mess_log,local_log):
        pass
    else:
        f = codecs.open(mess_log,"r",encoding= "utf-8")
        value = f.read()
        forms.alert(value, ok = True)

        shutil.copyfile(mess_log,local_log)
else:
    shutil.copyfile(mess_log,local_log)
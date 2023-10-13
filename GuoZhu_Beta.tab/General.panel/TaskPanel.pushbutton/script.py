# -*- coding: utf-8 -*-
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("IronPython.Wpf")

import wpf
from System import Windows

import codecs
import datetime

#find the path of ui XAML
from pyrevit import forms,script

#xmal_file = script.get_bundle_file("ui.xaml")
xmal_file = "C:\\Users\\6321011\\Desktop\\firstWPFApp\\firstWPFApp\\firstWPFApp\\ui.xaml"

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self,xmal_file)


MyWindow().ShowDialog()

# mess_log = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\worklog\\message_log.txt"
# try:
#     value = forms.ask_for_string(
        
#         prompt='Enter new tag name:',
#         title='Tag Manager'
#     )


#     if value is None:
#         script.excit()
#     else:
#         x = datetime.datetime.now()
#         time = x.strftime("%X")
#         messSend = value + "          -" + time

#         f = codecs.open(mess_log,"w",encoding = "utf-8")
#         f.write(messSend)
#         f.close
# except:
#     pass
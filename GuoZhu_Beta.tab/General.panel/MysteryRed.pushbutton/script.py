# -*- coding: utf-8 -*-
import clr

from pyrevit import forms	

from Autodesk.Revit.ApplicationServices import *
from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from pyrevit import forms


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = uidoc.ActiveView
uiapp = UIApplication(doc.Application)


res = forms.alert("发生致命错误。应用程序将被终止。您有机会保存所有更改项目的恢复文件。\n"

    "                   \n"
    "是否要保存恢复文件？",

    options=["保存","不保存"])

def my_pop1():
    forms.alert("确定不保存？", options = ["保存","不保存"])

def my_pop2():
    forms.alert("保存失败", options = ["重试"])

def my_function():
    dialog = TaskDialog("保存中")
    dialog.MainInstruction = "保存中"
    dialog.MainContent = "努力保存中"
    dialog.AllowCancellation = True
    dialog.CommonButtons = TaskDialogCommonButtons.Retry
    dialog.EnableMarqueeProgressBar = True


    result = dialog.Show()



if res == "保存":
    for i in range(5):
       my_function() 

else:
    my_pop1()
    for i in range(5):
        my_pop2()
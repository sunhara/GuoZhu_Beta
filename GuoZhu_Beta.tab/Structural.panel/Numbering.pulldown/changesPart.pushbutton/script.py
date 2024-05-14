# -*- coding: utf-8 -*-
import clr
import codecs
import os

from pyrevit import forms, script
from Autodesk.Revit.DB import*
from Autodesk.Revit.DB import UnitTypeId

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

docProject = doc.ProjectInformation.Name


partsLog_path = "\\\\10.1.37.5\国住共享文件夹\国住设计区\设计共享区\BIM项目\项目-Project\\1Aa_WorkLogs\{}\partslog.txt".format(docProject)


eleList = []       

with codecs.open(partsLog_path,'r',encoding='utf-8') as f:

    
    for line in f:
        eleList.append(line.rstrip())


t = Transaction(doc,"New Transaction")
t.Start()
elements = list(set([doc.GetElement(ElementId(int(i))) for i in eleList]))

for i in elements:
    try:
        targetPara = i.LookupParameter("Internal_modified")
        
        targetPara.Set("Changed")
    except:
        pass
t.Commit()


# Erase the list
if t.GetStatus() == TransactionStatus.Committed:

    with codecs.open(partsLog_path,'w',encoding='utf-8') as f:
        f.write('')
else:
    pass        
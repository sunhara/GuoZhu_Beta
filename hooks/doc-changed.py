# -*- coding: utf-8 -*-
import codecs
from datetime import datetime
import os
# from Autodesk.Revit.DB import*

from pyrevit import EXEC_PARAMS

args = EXEC_PARAMS.event_args
doc = args.GetDocument()

#function for detecting action
def detect(args): 
    docAdde = args.GetAddedElementIds()
    docDel = args.GetDeletedElementIds()
    docModi = args.GetModifiedElementIds()
    if len(docAdde) != 0:
        return "add"
    elif len(docDel) != 0:
        return "del"
    else: 
        return "modi"

#Getting the necessary info
try:
    
    docName = str(args.GetDocument().Title)
    docProject = str(args.GetDocument().ProjectInformation.Name)
    
    #Action detection
    action = detect(args)

    #time data
    time = datetime.now()
    dateStr = time.strftime("%Y-%m-%d")
    timeStr = time.strftime("%H-%M-%S")

    #Setup the path or create new path
    filepath = "\\\\10.1.37.5\国住共享文件夹\国住设计区\设计共享区\BIM项目\项目-Project\\1Aa_WorkLogs\{}\worklog.txt".format(docProject)
    newfilepath = "\\\\10.1.37.5\国住共享文件夹\国住设计区\设计共享区\BIM项目\项目-Project\\1Aa_WorkLogs\{}".format(docProject)

    

    if not os.path.exists(filepath):
        os.makedirs(newfilepath)
        f = open("worklog.txt","w")
        f.close
    else:
        pass
    try:
        
        with codecs.open(filepath,'a',encoding='utf-8') as f:
            f.write(dateStr+"_"+timeStr+"_"+action+"_"+docName+"\n")

    except:
        pass


except:
    pass

#log in modified element id 
try:
    #Setup the path or create new path
    partsLog_path = "\\\\10.1.37.5\国住共享文件夹\国住设计区\设计共享区\BIM项目\项目-Project\\1Aa_WorkLogs\{}\partslog.txt".format(docProject)

    elemIds = args.GetModifiedElementIds()

    try:
        for i in elemIds:
            
            with codecs.open(partsLog_path,'a',encoding='utf-8') as f:
                f.write("{}".format(i.IntegerValue)+"\n")

    except:
        pass

except:
    pass
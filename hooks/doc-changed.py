# -*- coding: utf-8 -*-
import codecs
from datetime import datetime
import os

from pyrevit import EXEC_PARAMS

args = EXEC_PARAMS.event_args

#Getting the necessary info
try:
    docName = str(args.GetDocument().Title)
    docProject = str(args.GetDocument().ProjectInformation.Name)

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
            f.write(dateStr+"_"+timeStr+"_"+docName+"\n")

    except:
        pass


except:
    pass
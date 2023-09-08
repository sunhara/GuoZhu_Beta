# -*- coding: utf-8 -*-
import clr
clr.AddReference('System')
from System.Collections.Generic import List
import json
import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import forms	
from pyrevit import script

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

#Getting selected drafting views from the doc
selection = uidoc.Selection.GetElementIds()
details = [doc.GetElement(e) for e in selection]


for i in details:
    detName = i.Name
    detId = i.Id

    # Define the image export options
    image_options = ImageExportOptions()
    image_options.ExportRange.VisibleRegionOfCurrentView

    #image_options.ExportRange = expRange
    image_options.HLRandWFViewsFileType = ImageFileType.JPEGMedium

    # image file path
    targetPath = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\2D大样图集\\{}.jpg".format(detName)
    image_options.FilePath = targetPath
    
    #Export all images
    uidoc.ActiveView = i
    doc.ExportImage (image_options)


    #close the view when its done
    uiviews = uidoc.GetOpenUIViews()
    for i in uiviews:
        if i.ViewId == detId:

            try:
                i.Close()
            except:
                    forms.alert("需要至少一个打开窗口", exitscript=True)
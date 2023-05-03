# -*- coding: utf-8 -*-
import json	

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')


from pyrevit import forms

#import Autodesk	
from Autodesk.Revit.DB import * #Loading Revit's API classes
from Autodesk.Revit.UI import * #Loading Revit's API UI classes  
from Autodesk.Revit.ApplicationServices import *


# Define the path 
file_path = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\材料仓库-Adsklib\\Materials Box\\Materials Library.rfa"

# Create a new application instance
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

uiapp = UIApplication(app)
uidoc = __revit__.ActiveUIDocument


fam_doc = app.OpenDocumentFile(file_path)

CmndID1 = RevitCommandId.LookupCommandId("ID_TRANSFER_PROJECT_STANDARDS")
CmndID2 = RevitCommandId.LookupPostableCommandId(PostableCommand.Save)

print(CmndID1)
print(CmndID2)

uiapp.PostCommand(CmndID1)
# Open the Revit file and create a new document object






# Do something with the Revit file here...

# Save and close the document
#fam_doc.Close(False)

#print (json.dumps(tuples,encoding ='utf-8',ensure_ascii=False))
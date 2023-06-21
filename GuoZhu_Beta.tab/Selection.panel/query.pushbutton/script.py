# -*- coding: utf-8 -*-
import clr
import json


clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import*



doc = __revit__
doc1 = Autodesk.Revit.UI.ExternalCommandData.Application
app = UIApplication()
doc2 = app.ActiveUIDocument.Document



#app = __revit__.Application


# active_view = doc.ActiveView
# uiapp = UIApplication(doc.Application)


print(doc)
print(doc2)

# print("--"*50)
# print(json.dumps(groupNames,encoding ='utf-8',ensure_ascii=False))
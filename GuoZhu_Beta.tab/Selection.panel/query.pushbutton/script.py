# -*- coding: utf-8 -*-
import clr

import json

clr.AddReference('System')
from System.Collections.Generic import List


import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import forms,script

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

# Creating collector instance and collecting all the stiffeners from the model
collector1 = FilteredElementCollector(doc).WhereElementIsNotElementType().OfClass(SharedParameterElement)



for elem in collector1:
    
    param_def = elem.GetDefinition()
    uID = elem.UniqueId
    print("{} - {}".format(elem.Name,uID))
    

    # print(json.dumps(elem.Name,encoding ='utf-8',ensure_ascii=False))

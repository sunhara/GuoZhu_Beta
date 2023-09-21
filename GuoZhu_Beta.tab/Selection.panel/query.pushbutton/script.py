# -*- coding: utf-8 -*-
import clr
import codecs
import os
import shutil
import filecmp
import datetime

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import *

class ElementToCopy(forms.TemplateListItem):
    @property
    def name(self):
        return self.Name

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

x = datetime.datetime.now()
time = x.strftime("%X")

print(time)
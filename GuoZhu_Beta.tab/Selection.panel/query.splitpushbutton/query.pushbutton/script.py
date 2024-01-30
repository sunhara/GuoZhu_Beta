# -*- coding: utf-8 -*-
import json	
import clr
import math
import xml.etree.ElementTree as ET

from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

selection = uidoc.Selection.GetElementIds()

file = "C:/Users/6321011/Desktop/textXML.xml"
tree = ET.parse(file)
root = tree.getroot()

for i in root.findall("country"):
    rank = i.find("rank").text
    name = i.get("name")
    print(rank,name)

for rank in root.iter('rank'):
     new_rank = int(rank.text) + 1
     rank.text = str(new_rank)
     rank.set('updated', 'yes')

tree.write("C:/Users/6321011/Desktop/output.xml")
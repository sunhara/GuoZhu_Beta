# -*- coding: utf-8 -*-
import clr

clr.AddReference('System')
clr.AddReference("System.Windows.Forms")


from System.Windows.Forms import  OpenFileDialog

from pyrevit import forms,script	
import Autodesk

from Autodesk.Revit.UI import*
from Autodesk.Revit.DB import*
from Autodesk.Revit.ApplicationServices import *

#opendialog setting
dialog = OpenFileDialog()
dialog.Filter = "All Files|*.rfa"
dialog.Multiselect = False
dialog.InitialDirectory = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\库-Family\\结构部件-Family\\Collaborate AS-Family"

class ElementToCopy(forms.TemplateListItem):
    @property
    def name(self):
        return self.Name

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

active_view = doc.ActiveView
uiapp = UIApplication(doc.Application)

# Define the source path 
dialog.ShowDialog()
file_path = dialog.FileName


try:
    fam_doc = app.OpenDocumentFile(file_path)
except:
    script.exit()

#Source family types
famTypes = [i for i in fam_doc.FamilyManager.Types]
famTypeNames = [i.Name for i in fam_doc.FamilyManager.Types]


options = [ElementToCopy(e) for e in famTypes]
elesToImport = forms.SelectFromList.show(options, title = "选择类型导入", width = 500, button_name = "导入", multiselect = True)
#Script exict point
if not elesToImport:
    fam_doc.Close(False)
    script.exit()


t = Transaction(doc,"Copy Elements")
t.Start()

for i in elesToImport:
    doc.LoadFamilySymbol(file_path, i.Name)

t.Commit()

fam_doc.Close(False)
forms.alert("导入完成", exitscript=True)
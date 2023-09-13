# -*- coding: utf-8 -*-
import clr
clr.AddReference('System')
clr.AddReference("System.Windows.Forms")


from System.Windows.Forms import  OpenFileDialog

from System.Collections.Generic import List
import json
import Autodesk
from Autodesk.Revit.DB import*

from pyrevit import script

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
uidoc = __revit__.ActiveUIDocument

#Create new handler to hide and accept duplicate
class HideAndAcceptDuplicateTypeNamesHandler(IDuplicateTypeNamesHandler):

    def OnDuplicateTypeNamesFound(self, args):
        # Always use duplicate destination types when asked
        return DuplicateTypeAction.UseDestinationTypes


#selecting elements to copy
def ElementForCopy(names,details):
    eles = []
    for n in names:
        for dt in details:
            if n == dt.Name:
                eles.append(dt)

    return  eles


# Define the source path 
file_path = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\2D大样图集\\Details Collection.rvt"
det_doc = app.OpenDocumentFile(file_path)

#Source details
details = FilteredElementCollector(det_doc).OfClass(ViewDrafting).WhereElementIsNotElementType()
detNames = [e.Name for e in details]

#Destination details
doc_details = FilteredElementCollector(doc).OfClass(ViewDrafting).WhereElementIsNotElementType()
doc_detNames = [e.Name for e in doc_details]


#Create openfile dialog for selecting files
details_names = []

#opendialog setting
dialog = OpenFileDialog()
dialog.Filter = "All Files|*.JPG"
dialog.Multiselect = True
dialog.InitialDirectory = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\2D大样图集"

if dialog.ShowDialog():

    selectedFiles = dialog.SafeFileNames
    for i in selectedFiles:
        details_names.append(i[:-4])


elesToCopy = ElementForCopy(details_names,details)



#Script exict point
if not elesToCopy:
    det_doc.Close(False)
    script.exit()

#mockView for destination view. and it has to be drafting view
mockViews = FilteredElementCollector(doc).OfClass(ViewDrafting).WhereElementIsNotElementType().ToElements()
mockView = []
newViewNames = []

for i in mockViews:
    if i.IsTemplate == False:
        mockView.append(i)


#all the views to be copied

for i in elesToCopy:
    
    t = Transaction(doc,"Copy drafting view and content Elements")
    t.Start()



    #Copy view drafting settings
    newViewNames.append(i.Name)
    id =[i.Id]
    ids_copy= List[ElementId](id)
    
    #if the filtered elements has a view element will create a view
    details_elements = FilteredElementCollector(det_doc,id[0]).ToElementIds()
    ids_details_elements= List[ElementId](details_elements)

    copyOpts = CopyPasteOptions()
    trans = Transform.Identity

    #handler to hide and accept duplicate
    handler = HideAndAcceptDuplicateTypeNamesHandler()
    copyOpts.SetDuplicateTypeNamesHandler(handler)

    ElementTransformUtils.CopyElements(i,ids_details_elements,mockView[0],trans,copyOpts)


    t.Commit()
det_doc.Close(False)
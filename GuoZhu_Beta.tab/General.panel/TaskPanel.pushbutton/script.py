# -*- coding: utf-8 -*-
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("IronPython.Wpf")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")

import csv
import wpf
from System import Windows
import codecs

from System.ComponentModel import INotifyPropertyChanged
from System.ComponentModel import PropertyChangedEventArgs

#find the path of ui XAML
from pyrevit import forms,script

from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document

#xmal_file = script.get_bundle_file("ui.xaml")
xmal_file = "C:\\Users\\6321011\\Desktop\\firstWPFApp\\firstWPFApp\\firstWPFApp\\ui.xaml"
# The task log location
task_log = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\worklog\\task_log.txt"



# function for unique user names
user_names = []
all_3d_view = FilteredElementCollector(doc).OfClass(View3D).WhereElementIsNotElementType().ToElementIds()
for i in all_3d_view:
    user = WorksharingUtils.GetWorksharingTooltipInfo(doc,i).Creator
    user_names.append(user)

user_names = list(set(user_names))

# List of tasks

#function for extract index list from a list
def Extract(lst,i):
    return [item[i] for item in lst]

if task_log is not None:
    #Modified the csv data list
    modified_f = []
    piror_level = []
    if task_log:
        with codecs.open(task_log, 'r', encoding="UTF-8") as f:
            
            for row in csv.reader(f):
                # extract all strings
                modified_f.append(','.join(row))
                # extract all pirority levels
                piror_level.append(row[0].split(":")[0])


# The item in the ScrollViewer
class CheckBoxListItem:
    def __init__(self, contex, piror_level, isChecked=False):
        
        self.Contex = contex
        self.Pl = piror_level
        self.IsChecked = isChecked


# convert into object
# change the letter to different color blocks
listViewData = []
for name,level in zip(modified_f,piror_level):

    if level == "高":
        item = CheckBoxListItem(name,"Red")
        listViewData.append(item)

    elif level == "中":
        item = CheckBoxListItem(name,"Orange")
        listViewData.append(item)

    elif level == "低":
        item = CheckBoxListItem(name,"YellowGreen")
        listViewData.append(item)




class ViewModelBase(INotifyPropertyChanged):
    def __init__(self):
        self.propertyChangedHandlers = []

    def RaisePropertyChanged(self, propertyName):
        args = PropertyChangedEventArgs(propertyName)
        for handler in self.propertyChangedHandlers:
            handler(self, args)
            
    def add_PropertyChanged(self, handler):
        self.propertyChangedHandlers.append(handler)
        
    def remove_PropertyChanged(self, handler):
        self.propertyChangedHandlers.remove(handler)





class MyWindow(Windows.Window):
    

    def __init__(self):
        wpf.LoadComponent(self,xmal_file)
        
        self.assignTo.ItemsSource = user_names #self.vs.vsnames
        self.ListBox1.ItemsSource = listViewData
        


    #Post button
    def post(self,sender,args):
        
        # The Content.Name is the ComboBox Item's Grid's Name
        piror_level = self.pirority.SelectedValue.Content.Name
        inPutContext = self.context.Text
        user = self.assignTo.SelectedValue
        
        f = codecs.open(task_log,"a",encoding = "utf-8")
        f.write("{}:   {} - {}\n".format(piror_level,inPutContext,user))
        f.close
        self.Close()


    #Complete button
    def complete(self,sender,args):
        
        # The Content.Name is the ComboBox Item's Grid's Name
        selected_task = self.VisualTreeHelper.GetParent
        print(selected_task)


# MyWindow().Show()
MyWindow().ShowDialog()

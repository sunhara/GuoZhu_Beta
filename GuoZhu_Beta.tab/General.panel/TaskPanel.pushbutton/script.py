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

xmal_file = script.get_bundle_file("ui.xaml")
# xmal_file = "C:\\Users\\6321011\\Desktop\\firstWPFApp\\firstWPFApp\\firstWPFApp\\ui.xaml"
# The task log location
task_log = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\worklog\\task_log.txt"
task_log_completed = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\worklog\\task_log_completed.txt"


# function for unique user names
user_names = []
all_3d_view = FilteredElementCollector(doc).OfClass(View3D).WhereElementIsNotElementType().ToElementIds()
for i in all_3d_view:
    user = WorksharingUtils.GetWorksharingTooltipInfo(doc,i).Creator
    user_names.append(user)

user_names = list(set(user_names))



# List of tasks
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

# List of completed tasks
if task_log_completed is not None:
    #Modified the csv data list
    modified_f_c = []

    if task_log_completed:
        with codecs.open(task_log_completed, 'r', encoding="UTF-8") as f:
            
            for row in csv.reader(f):
                # extract all strings
                modified_f_c.append(','.join(row))


# remove the completed tasks
for i,j in zip(modified_f,piror_level):
    if i in modified_f_c:
        modified_f.remove(i)
        piror_level.remove(j)


# The item in the ScrollViewer
class CheckBoxListItem():
    def __init__(self, context, piror_level, index,isChecked=False):
        
        self.Context = context
        self.Pl = piror_level
        self.index = index
        self.IsChecked = isChecked



# convert into object
# change the letter to different color blocks
listViewData = []
for name,level in zip(modified_f,piror_level):

    if level == "高":
        item = CheckBoxListItem(name,"Red",1)
        listViewData.append(item)


    elif level == "中":
        item = CheckBoxListItem(name,"Orange",2)
        listViewData.append(item)

    elif level == "低":
        item = CheckBoxListItem(name,"YellowGreen",3)
        listViewData.append(item)


#sorted all the context by their pirority level index
newlistViewData = sorted(listViewData,key =lambda x: x.index)


class MyWindow(Windows.Window):
    

    def __init__(self):
        wpf.LoadComponent(self,xmal_file)
        
        self.assignTo.ItemsSource = user_names 
        self.ListBox1.ItemsSource = newlistViewData
        


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
        selected_task = self.ListBox1.ItemsSource
        for i in selected_task:
            if i.IsChecked:
                f = codecs.open(task_log_completed,"a",encoding = "utf-8")
                f.write("{}\n".format(i.Context))
                f.close
                self.Close()
        

# MyWindow().Show()
MyWindow().ShowDialog()
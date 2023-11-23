# -*- coding: utf-8 -*-
import sys
import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("IronPython.Wpf")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")

from System.IO import File
from System.Windows.Markup import XamlReader

import wpf
from System import Windows


from System.Windows import Application
from System.Windows.Media import Brushes

from System.ComponentModel import INotifyPropertyChanged
from System.ComponentModel import PropertyChangedEventArgs

#find the path of ui XAML
from pyrevit import forms,script

from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document

# xmal_file = script.get_bundle_file("ui.xaml")
xmal_file = "C:\\Users\\6321011\\Desktop\\firstWPFApp\\WpfApp2\\WpfApp2\\MainWindow.xaml"


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

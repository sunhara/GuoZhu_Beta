# -*- coding: utf-8 -*-
import clr


clr.AddReference('System')
from System.Collections.Generic import List


from pyrevit import forms,script

output = script.get_output()

from Autodesk.Revit.DB import*

selected_option, switches = \
    forms.CommandSwitchWindow.show(
        ['Option_1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'],
        switches=['Switch 1', 'Switch 2'],
        message='Select Option:',
        recognize_access_key=True
        )

if selected_option:
    print('Selected Option: {}'
          '\n Switch 1 = {}'
          '\n Switch 2 = {}'.format(selected_option,
                                    switches['Switch 1'],
                                    switches['Switch 2']))
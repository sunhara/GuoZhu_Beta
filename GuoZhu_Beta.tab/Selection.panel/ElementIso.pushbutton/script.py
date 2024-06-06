# -*- coding: utf-8 -*-
import json	
import clr
import uuid

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms	
from pyrevit import script

import Autodesk
from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = uidoc.ActiveView

# type:(List[ElementId], View) -> None
#Function to Isolate Elements in the given View.
def isolate_elements(elements, view):

    hide_elem = FilteredElementCollector(doc, view.Id).Excluding(elements).WhereElementIsNotElementType().ToElements()

    hide_elem_ids = [e.Id for e in hide_elem 
                      if e.CanBeHidden(view)]

    view.HideElements(List[ElementId](hide_elem_ids))


#input view name
value = forms.ask_for_string(
        
        prompt='输入视图名称:',
        title='View Title Input'
    )


try:

    elements_to_isolate = [doc.GetElement(e_id) 
            for e_id in uidoc.Selection.GetElementIds()]

    part_mark = elements_to_isolate[0].LookupParameter("工厂加工-零件标号").AsString()
    GUID = uuid.uuid4()
    

    if part_mark is not None and len(part_mark) != 0:

        #STAR THE TRANSACTION!!!
        t = Transaction(doc, 'Isolate Elements')
        t.Start()

        
        List_isolate_ids = uidoc.Selection.GetElementIds()

        #Created new view with name
        new_viewId = active_view.Duplicate(ViewDuplicateOption.Duplicate)
        new_view_ele = doc.GetElement(new_viewId)
        name = new_view_ele.get_Parameter(BuiltInParameter.VIEW_NAME)

        #Name for the View default or input
        if len(value)==0:

            name.Set(part_mark)
        else:
            name.Set(value)
        
        
        #isolate the element
        isolate_elements(List_isolate_ids, new_view_ele)

        #create bounding box and offset around element
        bbox = elements_to_isolate[0].get_BoundingBox(None)
        box_max = bbox.Max
        box_min = bbox.Min
        factor = 0.01
        new_box_max = box_max.Add(XYZ(factor,factor,factor))
        new_box_min = box_min.Add(XYZ(-factor,-factor,-factor))

        new_bbox = BoundingBoxXYZ()
        new_bbox.Max = new_box_max
        new_bbox.Min = new_box_min
        new_view_ele.SetSectionBox(new_bbox)


        t.Commit()

        # seconde transaction for assing guid to view and element
        t2 = Transaction(doc, 'assign GUID')
        t2.Start()

        targetEleGUID = elements_to_isolate[0].LookupParameter("视口关联GUID")
        targetEleGUID.Set(str(GUID))

        targetViewGUID = new_view_ele.LookupParameter("视口关联GUID")
        targetViewGUID.Set(str(GUID))

        t2.Commit()

    else :
        forms.alert('工厂加工-零件标号不能为空值', exitscript=True)

except:

    if elements_to_isolate == []:

        forms.alert('未选择模型物体', exitscript=True)
    else:
        pass

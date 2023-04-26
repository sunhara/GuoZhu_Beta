# -*- coding: utf-8 -*-
from pyrevit import forms	

from pyrevit import revit, DB, UI
from pyrevit import script


def who_created_selection():
    selection = revit.get_selection()
    if revit.doc.IsWorkshared:
        if selection and len(selection) == 1:
            eh = revit.query.get_history(selection.first)

            forms.alert('创建者:{0}\n''当前占用者: {1}\n''最后一次同步人: {2}'.format(eh.creator,eh.owner,eh.last_changed_by))
        else:
            forms.alert("先选择一个element")
    else:
        forms.alert("不是中心文件")


def who_created_activeview():
    active_view = revit.active_view
    view_id = active_view.Id.ToString()
    view_name = active_view.Name
    view_creator = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, active_view.Id).Creator

    forms.alert('{}{}{}'.format("视口名称：" + view_name, "视口ID: " + view_id,"创建者: " + view_creator))


options = {'谁创建了该视口?': who_created_activeview,
           '谁创建该模型': who_created_selection,
            }

selected_option = \
    forms.CommandSwitchWindow.show(options.keys())

if selected_option:
    options[selected_option]()
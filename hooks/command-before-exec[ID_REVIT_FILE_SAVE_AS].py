# -*- coding: utf-8 -*-

from pyrevit import HOST_APP, EXEC_PARAMS, forms


args = EXEC_PARAMS.event_args

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

central_model = doc.IsWorkshared

if central_model is True:
    
    credential = "1q2w3e4r"
    
    
    res = forms.alert("警告,中心文件禁止另存为\n"
                        "是否继续另存为？",yes = True, cancel = True, ok = False)

   
    if res:
        user_input = forms.ask_for_string(prompt = "管理员密码")
        if user_input != credential:
            args.Cancel = True
    else:
        args.Cancel = True

else:
    pass
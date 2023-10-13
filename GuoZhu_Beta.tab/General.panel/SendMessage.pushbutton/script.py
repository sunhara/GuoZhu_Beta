# -*- coding: utf-8 -*-
import codecs
import datetime

from pyrevit import forms,script

mess_log = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\worklog\\message_log.txt"
try:
    value = forms.ask_for_string(
        
        prompt='Send Gloabl Message:',
        title='Send Manager'
    )


    if value is None:
        script.excit()
    else:
        x = datetime.datetime.now()
        time = x.strftime("%X")
        messSend = value + "          -" + time

        f = codecs.open(mess_log,"w",encoding = "utf-8")
        f.write(messSend)
        f.close
except:
    pass
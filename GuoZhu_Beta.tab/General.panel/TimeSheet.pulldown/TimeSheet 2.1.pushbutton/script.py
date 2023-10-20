# -*- coding: utf-8 -*-
import clr
import csv 

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms	
from pyrevit import script
output = script.get_output()

from Autodesk.Revit.DB import*
from datetime import datetime, timedelta


#Convert to minutes
def ToMinute(t):  
    hours = float(t.total_seconds() / 60)
    return hours

#Calculate timedelta percentage
def TimePercentage(td1,td2):
    return td1.total_seconds()/td2.total_seconds()*100

#function for extract index list from a list
def Extract(lst,i):
    return [item[i] for item in lst]


# function strptime from string to dateobj
def ConvertDate (lst):
    date_objects = []
    for i in lst:
        date_object = datetime.strptime(i, "%Y-%m-%d_%H-%M-%S")
        date_objects.append(date_object)
    return date_objects

#function to calcualte total elapsed time
def TotalElap (lst):
    timeCollec = []
    lst.reverse()

    for i in range(len(lst)-1):
        
        timeElap =lst[i]-lst[i+1]
        
        if min_hour<timeElap< max_hour:
            timeCollec.append(timeElap)
        else:
            pass

    return timeCollec

max_hour = timedelta(seconds=30)
min_hour = timedelta(seconds=1)

# Define the file path
#source_file = "C:\\Users\\6321011\Desktop\\2301-锡小行政楼_结构_worklog.txt"
source_file = forms.pick_file(file_ext='txt')


#Modified the csv data list
modified_f = []
if source_file:
    with open(source_file, 'r') as f:
        next(f)
        for row in csv.reader(f):
            data = row[0].split("_")
            clean_data = list(filter(None, data))
            modified_f.append(clean_data)

    

#Sorted data by user name, user names are the last index of the list
#sorted_data = sorted(modified_f, key=lambda data: data[-1])
user_data = Extract(modified_f,-1)

# Each individual users name
unique_user = list(set(user_data))

#Calculate individual  user's time for different ratio
user_modi_time_str = []
user_add_time_str = []
user_del_time_str = []

#All modification time
for i in unique_user:
    usertime = []
    
    #Calculate individual user's time
    for dataRow in modified_f:
        
        if dataRow[-1] == i and dataRow[2] == "modi" :
            date = dataRow[0]
            time = dataRow[1]
            date_time = date+"_"+time
            usertime.append(date_time)
        else:
            pass
    user_modi_time_str.append(usertime)

#All adding time
for i in unique_user:
    usertime = []
    
    #Calculate individual user's time
    for dataRow in modified_f:
        
        if dataRow[-1] == i and dataRow[2] == "add" :
            date = dataRow[0]
            time = dataRow[1]
            date_time = date+"_"+time
            usertime.append(date_time)
        else:
            pass
    user_add_time_str.append(usertime)

#All del time
for i in unique_user:
    usertime = []
    
    #Calculate individual user's time
    for dataRow in modified_f:
        
        if dataRow[-1] == i and dataRow[2] == "del" :
            date = dataRow[0]
            time = dataRow[1]
            date_time = date+"_"+time
            usertime.append(date_time)
        else:
            pass
    user_del_time_str.append(usertime)



# #Collecting total time and calculation in different ratio
user_del_time = []
for i in user_del_time_str:
    time_obj =ConvertDate(i)
    timeCollec = TotalElap(time_obj)
    total_time = sum(timeCollec, timedelta())
    user_del_time.append(total_time)
    
user_add_time = []
for i in user_add_time_str:
    time_obj =ConvertDate(i)
    timeCollec = TotalElap(time_obj)
    total_time = sum(timeCollec, timedelta())
    user_add_time.append(total_time)

user_modi_time = []
for i in user_modi_time_str:
    time_obj =ConvertDate(i)
    timeCollec = TotalElap(time_obj)
    total_time = sum(timeCollec, timedelta())
    user_modi_time.append(total_time)


outData = []
for i,j,k,l in zip(unique_user,user_add_time,user_modi_time,user_del_time):
    if ToMinute(j)+ToMinute(k)+ToMinute(l) ==0:
        pass
    else:
        sumtotal = ToMinute(j)+ToMinute(k)+ToMinute(l)
        outData.append([i,ToMinute(j)/sumtotal*100,ToMinute(k)/sumtotal*100,ToMinute(l)/sumtotal*100])

# sum up different ratio time
total_add_time = sum(user_add_time, timedelta())
total_modi_time = sum(user_modi_time, timedelta())
total_del_time = sum(user_del_time, timedelta())

ttc = total_add_time+total_modi_time+total_del_time

#append to the last row
outData.append([])
outData.append(["整体项目时间占比",TimePercentage(total_add_time,ttc)
                              ,TimePercentage(total_modi_time,ttc)
                              ,TimePercentage(total_del_time,ttc)])


# formats contains formatting strings for each column
output.print_table(table_data=outData,
                   title="BIM有效操作时间比例",
                   columns=["人员", "添加占比", "修改占比", "删除占比"],
                   formats=['', '{} %', '{} %', '{} %'],
                   last_line_style='color:blue;'
                   )

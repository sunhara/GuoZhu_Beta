# -*- coding: utf-8 -*-

import clr
import csv 

clr.AddReference('System')
from System.Collections.Generic import List

from pyrevit import forms	
from pyrevit import script

from Autodesk.Revit.DB import*
from datetime import datetime, timedelta

def Extract(lst,i):
    return [item[i] for item in lst]

def converDate (lst):
    date_objects = []
    for i in lst:
        date_object = datetime.strptime(i, "%Y/%m/%d %H:%M:%S")
        date_objects.append(date_object)
    return date_objects

def totalElap (lst):
    timeCollec = []

    for i in range(len(lst)-1):
        
        timeElap =lst[i]-lst[i+1]
        
        if min_hour<timeElap< max_hour:
            timeCollec.append(timeElap)
        else:
            pass

    return timeCollec

max_hour = timedelta(minutes=59)
min_hour = timedelta(seconds=20)

# Define the file path
#source_file = "C:\\Users\\6321011\Desktop\\2301-锡小行政楼_结构_Central_2023 History.txt"
source_file = forms.pick_file(file_ext='txt')

#Modified the csv data list
modified_f = []
if source_file:
    with open(source_file, 'r') as f:
        next(f)
        for row in csv.reader(f):
            data = row[0].split("\t")
            clean_data = list(filter(None, data))
            modified_f.append(clean_data)
      
     
#List [list](modified_f)

sorted_data = sorted(modified_f, key=lambda data: data[1])

time_data = Extract(sorted_data,0)
user_data = Extract(sorted_data,1)
unique_user = list(set(user_data))



individual_user_time = []
for i in unique_user:
    sublist = [x for x in sorted_data if x[1] ==i]
    individual_user_time.append(Extract(sublist,0))





#Collecting total time and calculation   

total_date = converDate(time_data)

timeCollec = totalElap(total_date)

total_time = sum(timeCollec, timedelta())

user_time = []

for i in individual_user_time:
    date = converDate(i)
    time = totalElap(date)
    total = sum(time, timedelta())
    user_time.append(total)

timeSec_int = []
for t in user_time:
    hours = int(t.total_seconds() / 3600)
    timeSec_int.append(hours)


output = script.get_output()
chart = output.make_pie_chart()

# Set the labels for the circumference axis
chart.data.labels = unique_user

# Create new data sets
set_a = chart.data.new_dataset('set_a')
set_a.data = timeSec_int

chart.randomize_colors()

chart.draw()



txt= "总时间:  {}"
print(txt.format(total_time))
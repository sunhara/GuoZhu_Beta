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

if source_file is not None:
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

    #Calculate individual  user's time
    individual_user_time_str = []


    for i in unique_user:
        usertime = []
        
        #Calculate individual user's time
        for dataRow in modified_f:
            
            if dataRow[-1] == i:
                date = dataRow[0]
                time = dataRow[1]
                date_time = date+"_"+time
                usertime.append(date_time)
            else:
                pass
        individual_user_time_str.append(usertime)


    #Collecting total time and calculation   
    individual_user_time = []

    for i in individual_user_time_str:
        time_obj =ConvertDate(i)
        time_obj.sort
        timeCollec = TotalElap(time_obj)
        total_time = sum(timeCollec, timedelta())
        individual_user_time.append(total_time)
        


    for i,j in zip(unique_user,individual_user_time):
        txt = "{}  建模时间:  {}"
        print(txt.format(i,j))

    project_totaltime = sum(individual_user_time, timedelta())



    timeSec_int = []
    for t in individual_user_time:
        hours = int(t.total_seconds() / 3600)
        timeSec_int.append(hours)


    #Creating pie chart
    chart = output.make_pie_chart()

    # Set the labels for the circumference axis
    chart.data.labels = unique_user

    # Create new data sets
    set_a = chart.data.new_dataset('set_a')
    set_a.data = timeSec_int

    chart.randomize_colors()
    chart.draw()

    txt= "总时间:  {}"
    print(txt.format(project_totaltime))
    
else:
    pass
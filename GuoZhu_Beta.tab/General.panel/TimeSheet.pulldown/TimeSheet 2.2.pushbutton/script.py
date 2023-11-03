# -*- coding: utf-8 -*-
import clr
import csv 

clr.AddReference('System')
from System.Collections.Generic import List

from itertools import groupby

from pyrevit import forms	
from pyrevit import script
output = script.get_output()

from Autodesk.Revit.DB import*
from datetime import datetime, timedelta


def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
         flat_list.extend(row)
    return flat_list

#function for extract index list from a list
def Extract(lst,i):
    return [item[i] for item in lst]


# function strptime from string to dateobj
def ConvertDate (i):
    
    date_object = datetime.strptime(i, "%Y-%m-%d_%H-%M-%S")  
    return date_object

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

max_hour = timedelta(seconds =30)
min_hour = timedelta(seconds =1)

# Define the file path
# Test log above
# source_file = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\项目-Project\\1Aa_WorkLogs\\长安学校#1\\worklog.txt"
# source_file = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\项目-Project\\1Aa_WorkLogs\\西城区三帆中学学位应急保障工程\\worklog.txt"
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


    # Each logged date
    daily_date = Extract(modified_f,0)
    unique_date = list(set(daily_date))
    unique_date.sort()

    #Calculate individual  user's time

    daily_time_list = []


    for i in unique_date:
        log_date = []

        #Calculate individual user's time
        for user in unique_user:
            usertime = []
            for dataRow in modified_f:
                
                if dataRow[0] == i and dataRow[-1] == user:
                    date = dataRow[0]
                    time = dataRow[1]
                    date_time = date+"_"+time

                    usertime.append(ConvertDate(date_time))
                    
                else:
                    x = datetime(1111, 11, 11)
                    usertime.append(x)

            log_date.append(usertime)

        daily_time_list.append(log_date)


    user_date_time = []

    for i in daily_time_list:

        temp_date_time = []
        for timeObj in i:
            # timeObj needs to sort
            timeObj.sort()
            timeCollec = TotalElap(timeObj)
            total_time = sum(timeCollec, timedelta())
            temp_date_time.append(total_time)


        user_date_time.append(temp_date_time)
    
        

    for i,j in zip(user_date_time,unique_date):
        i.insert(0,j)


    unique_user.insert(0,"Date")

    # print(user_date_time)
    output.print_table(table_data=user_date_time,
                   title="Daily Time",
                   columns=unique_user,
                   formats=[]
                   )
    

else:
    pass
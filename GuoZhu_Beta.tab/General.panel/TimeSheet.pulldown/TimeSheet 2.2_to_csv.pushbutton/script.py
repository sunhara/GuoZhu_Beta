#! python3
import sys
import csv 

sys.path.append("\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\Lib\\site-packages")

import pandas as pd
import numpy as np
import os

from System.Windows.Forms import  OpenFileDialog
from tabulate import tabulate

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
def ConvertDate2 (i):
    
    date_object = datetime.strptime(i, "%H-%M-%S")  
    return date_object


max_hour = timedelta(seconds =30)
min_hour = timedelta(seconds =1)

# Define the file path
# Test log below
# source_file = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\项目-Project\\1Aa_WorkLogs\\长安学校#1\\worklog.txt"
# source_file = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\项目-Project\\1Aa_WorkLogs\\西城区三帆中学学位应急保障工程\\worklog.txt"

#opendialog setting
dialog = OpenFileDialog()

dialog.Multiselect = True
dialog.InitialDirectory = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\项目-Project\\1Aa_WorkLogs"

try:
    dialog.ShowDialog()
    source_file = dialog.FileName
    #title for the csv file
    file_name = (source_file.split('\\')[-2]).split('.')[0]

    # #Script exict point
    # if not source_file:
    #     sys.exit()


    #Modified the csv data list
    modified_f = []
    if source_file:
        with open(source_file, 'r',encoding = "utf -8") as f:
            next(f)
            for row in csv.reader(f):
                data = row[0].split("_")
                clean_data = list(filter(None, data))

                # This func is to eliminate data created from the 
                # central file which has no user name!
                modified_f.append(clean_data) if len(clean_data)== 8 else next


    user_name = Extract(modified_f,-1)

    user_date = Extract(modified_f,0)
    user_time = [ConvertDate2(i) for i in Extract(modified_f,1)]


    #Setting for pandas
    pd.options.display.max_rows = 9999
    pd.options.display.width = 1200
    pd.options.display.max_colwidth = 100
    pd.options.display.max_columns = 100

    # data = [user_date,user_time,user_name]

    data = {
    "Date" : user_date,
    "TimeStamp" : user_time,
    "Name" : user_name
    }

    # df = pd.DataFrame(data).transpose()
    df = pd.DataFrame(data)

    # df.Time.astype(str).str.replace('0 days ', '')

    gr_df = df.groupby(["Date","Name"])

    frames = []

    for key, item in gr_df:

    
        item["TimeStamp"] = item["TimeStamp"].diff(1)
        item.dropna(inplace = True)

        #filter rows by multiple conditions
        item = item[(min_hour<item["TimeStamp"])& (item["TimeStamp"]< max_hour)]

        #daily_time = item["TimeStamp"].sum()
        newitem = item.groupby(["Date","Name"]).agg({'TimeStamp': 'sum'}).reset_index()

        frames.append(newitem)


    result_df = pd.concat(frames)
    # Remove days in timedelta
    result_df["TimeStamp"] = result_df["TimeStamp"].astype(str).str.split(' ').str[-1]


    newdf = result_df.pivot(index='Date', columns='Name', values='TimeStamp')

    '''
    On Windows, many editors assume the default ANSI encoding (CP1252 on US Windows) instead of UTF-8 
    encoding='utf-8-sig' or encoding='utf-16 works as well 
    '''
    
    file_path = os.environ['USERPROFILE'] + '\Desktop'

    newdf.to_csv("{}\\{}-时间表.csv".format(file_path,file_name),encoding='utf-8-sig')
    
    # print(newdf)
    #print(tabulate(newdf,headers = "keys",tablefmt = "github",maxcolwidths=[None, 50]))
except:
    pass
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import pandas as pd
from datetime import datetime, timedelta 


# In[2]:


insulin_df = pd.read_csv('InsulinAndMealIntake670GPatient3.csv')
insulin_df.head(5)


insulin_df = insulin_df.dropna(axis=0, subset=['BWZ Carb Input (grams)'])

insulin_df =insulin_df[insulin_df['BWZ Carb Input (grams)'] !=0]

insulin_df.head(5)

insulin_df.dtypes

#insulin_df = insulin_df.astype({'object' : 'Date'})

insulin_df['Date time'] = pd.to_datetime(insulin_df['Date'] + ' ' + insulin_df['Time'])
insulin_df.to_csv('insulin_trial1.csv', index=False)

cgm_df = pd.read_csv('CGMData670GPatient3.csv')
cgm_df.head(5)

cgm_df['Date time'] = pd.to_datetime(cgm_df['Date'] + ' ' + cgm_df['Time'])
cgm_df.to_csv('cgm_trial1.csv', index=False)

insulin_df['new_col'] = range(1, len(insulin_df) + 1)
insulin_df = insulin_df.set_index('new_col')
insulin_df.head(5)

# insulin_df #
# printing from reverse #

from datetime import datetime, timedelta 

#for i in range(1,len(insulin_df)+1):   #print from top
count = 0
for i in range(len(insulin_df),0,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    #print(start_time)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    #print(end_time)
    count += 1
#print("count is",count)

print(len(insulin_df)+1)

# this is for meal data -  no #
start_list = []
end_list = []

for i in range(len(insulin_df),1,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    if insulin_df.at[i-1, 'Date time']  > end_time:
        #dict1[start_time] = end_time
        start_list.append(start_time)
        end_list.append(end_time)        
    elif insulin_df.at[i-1, 'Date time'] == end_time:
        start = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 1) + timedelta(minutes = 30)
        end = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 4)    
        #dict1[start_time] = end_time
        start_list.append(start)
        end_list.append(end) 
#dict1[insulin_df.at[1, 'Date time'] - timedelta(minutes = 30)] = insulin_df.at[1, 'Date time'] + timedelta(hours = 2)

cgm_df['Meal or no meal']  = ""
cgm_df.head(5)

cgm_df.to_csv('cgm_trial.csv', index=False)

#print(len(cgm_df))

#len(start_list)

# this is for no meal data #


from datetime import datetime, timedelta 

#for i in range(1,len(insulin_df)+1):   #print from top
count = 0
for i in range(len(insulin_df),0,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    #print(start_time)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    #print(end_time)
    count += 1
#print("count is",count)

# creating start and end time for BOTH meal and no meal data #

from datetime import datetime, timedelta 
start_list = []
end_list = []

start_list_nm = []
end_list_nm = []

for i in range(len(insulin_df),1,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    if insulin_df.at[i-1, 'Date time']  > end_time:
        #dict1[start_time] = end_time
        start_list.append(start_time)
        end_list.append(end_time)
        
        if insulin_df.at[i-1, 'Date time']  > end_time + timedelta(hours = 2):
            start_list_nm.append(end_time)
            end_list_nm.append(end_time + timedelta(hours = 2))

    elif insulin_df.at[i-1, 'Date time'] == end_time:
        start = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 1) + timedelta(minutes = 30)
        end = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 4)    
        #dict1[start_time] = end_time
        start_list.append(start)
        end_list.append(end) 
        
        if insulin_df.at[i-1, 'Date time']  > end_time + timedelta(hours = 2):
            start_list_nm.append(end_time)
            end_list_nm.append(end_time + timedelta(hours = 2))
            
# meal data - creating lists to append#

list1= []
for j in range(len(start_list)):
    list2 = []
    t = 0
    for i in range(len(cgm_df)):
        if start_list[j] <= cgm_df.at[i, 'Date time'] and cgm_df.at[i, 'Date time'] <= end_list[j]:
        #cgm_df.loc[(cgm_df['Date time'] >= start_list[j]) & (cgm_df['Date time'] < end_list[j])]
            cgm_df.at[i,'Meal or no meal'] = 1
            if pd.isna(cgm_df.at[i,'Sensor Glucose (mg/dL)']):
                t += 1
            list2.append(cgm_df.at[i,'Sensor Glucose (mg/dL)'])
    if t == 0 and len(list2) == 30:
        list1.append(list2)


# nomeal data - creating lists to append#

list3 = []
for j in range(len(start_list_nm)):
    list4 = []
    t1 = 0
    for i in range(len(cgm_df)):
        if start_list_nm[j] <= cgm_df.at[i, 'Date time'] and cgm_df.at[i, 'Date time'] <= end_list_nm[j]:
        #cgm_df.loc[(cgm_df['Date time'] >= start_list[j]) & (cgm_df['Date time'] < end_list[j])]
            cgm_df.at[i,'Meal or no meal'] = 0
            if pd.isna(cgm_df.at[i,'Sensor Glucose (mg/dL)']):
                t1 += 1
            list4.append(cgm_df.at[i,'Sensor Glucose (mg/dL)'])
    if t1 == 0 and len(list4) == 24:
        list3.append(list4)

# download the mealdata.csv file #

import csv

with open("mealdata1.csv","w+", newline='') as my_csv:
    csvWriter = csv.writer(my_csv)
    csvWriter.writerows(list1)

# drop  last six columnns in meal data #

meal_df = pd.read_csv("mealdata1.csv") 

for i in range(6):
    meal_df = meal_df.drop(meal_df.columns[-1],axis=1)

meal_df.to_csv('mealdata1.csv',index=False)

# download the nomealdata.csv file #

with open("nomealdata1.csv","w+", newline='') as my_csv:
    csvWriter = csv.writer(my_csv)
    csvWriter.writerows(list3)

#len(list1)


# In[3]:



insulin_df = pd.read_csv('InsulinData.csv')
#insulin_df.head(5)

#df = df[pd.notnull(df['Gender'])]
#insulin_df = insulin_df[pd.notnull(insulin_df['BWZ Carb Input (grams)'])]
insulin_df = insulin_df.dropna(axis=0, subset=['BWZ Carb Input (grams)'])

insulin_df =insulin_df[insulin_df['BWZ Carb Input (grams)'] !=0]

#insulin_df.head(5)

insulin_df['Date time'] = pd.to_datetime(insulin_df['Date'] + ' ' + insulin_df['Time'])
insulin_df.to_csv('insulin_trial.csv', index=False)

cgm_df = pd.read_csv('CGMData.csv')
#cgm_df.head(5)

cgm_df['Date time'] = pd.to_datetime(cgm_df['Date'] + ' ' + cgm_df['Time'])
cgm_df.to_csv('cgm_trial.csv', index=False)

insulin_df['new_col'] = range(1, len(insulin_df) + 1)
insulin_df = insulin_df.set_index('new_col')
#insulin_df.head(5)

# insulin_df #
# printing from reverse #

#for i in range(1,len(insulin_df)+1):   #print from top
count = 0
for i in range(len(insulin_df),0,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    #print(start_time)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    #print(end_time)
    count += 1
#print("count is",count)

print(len(insulin_df)+1)

# this is for meal data -  no #

start_list = []
end_list = []

for i in range(len(insulin_df),1,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    if insulin_df.at[i-1, 'Date time']  > end_time:
        #dict1[start_time] = end_time
        start_list.append(start_time)
        end_list.append(end_time)        
    elif insulin_df.at[i-1, 'Date time'] == end_time:
        start = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 1) + timedelta(minutes = 30)
        end = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 4)    
        #dict1[start_time] = end_time
        start_list.append(start)
        end_list.append(end) 
#dict1[insulin_df.at[1, 'Date time'] - timedelta(minutes = 30)] = insulin_df.at[1, 'Date time'] + timedelta(hours = 2)

cgm_df['Meal or no meal']  = ""
#cgm_df.head(5)

cgm_df.to_csv('cgm_trial.csv', index=False)

#print(len(cgm_df))

#len(start_list)

# this is for no meal data #

#for i in range(1,len(insulin_df)+1):   #print from top
count = 0
for i in range(len(insulin_df),0,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    #print(start_time)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    #print(end_time)
    count += 1
#print("count is",count)

# creating start and end time for BOTH meal and no meal data #
 
start_list = []
end_list = []

start_list_nm = []
end_list_nm = []

for i in range(len(insulin_df),1,-1):
    start_time = insulin_df.at[i, 'Date time'] - timedelta(minutes = 30)
    end_time = insulin_df.at[i, 'Date time'] + timedelta(hours = 2)
    if insulin_df.at[i-1, 'Date time']  > end_time:
        #dict1[start_time] = end_time
        start_list.append(start_time)
        end_list.append(end_time)
        
        if insulin_df.at[i-1, 'Date time']  > end_time + timedelta(hours = 2):
            start_list_nm.append(end_time)
            end_list_nm.append(end_time + timedelta(hours = 2))

    elif insulin_df.at[i-1, 'Date time'] == end_time:
        start = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 1) + timedelta(minutes = 30)
        end = insulin_df.at[i-1, 'Date time'] + timedelta(hours = 4)    
        #dict1[start_time] = end_time
        start_list.append(start)
        end_list.append(end) 
        
        if insulin_df.at[i-1, 'Date time']  > end_time + timedelta(hours = 2):
            start_list_nm.append(end_time)
            end_list_nm.append(end_time + timedelta(hours = 2))
        

#dict1[insulin_df.at[1, 'Date time'] - timedelta(minutes = 30)] = insulin_df.at[1, 'Date time'] + timedelta(hours = 2)

# meal data - creating lists to append#

list1= []
for j in range(len(start_list)):
    list2 = []
    t = 0
    for i in range(len(cgm_df)):
        if start_list[j] <= cgm_df.at[i, 'Date time'] and cgm_df.at[i, 'Date time'] <= end_list[j]:
        #cgm_df.loc[(cgm_df['Date time'] >= start_list[j]) & (cgm_df['Date time'] < end_list[j])]
            cgm_df.at[i,'Meal or no meal'] = 1
            if pd.isna(cgm_df.at[i,'Sensor Glucose (mg/dL)']):
                t += 1
            list2.append(cgm_df.at[i,'Sensor Glucose (mg/dL)'])
    if t == 0 and len(list2) == 30:
        list1.append(list2)


# nomeal data - creating lists to append#

list3 = []
for j in range(len(start_list_nm)):
    list4 = []
    t1 = 0
    for i in range(len(cgm_df)):
        if start_list_nm[j] <= cgm_df.at[i, 'Date time'] and cgm_df.at[i, 'Date time'] <= end_list_nm[j]:
        #cgm_df.loc[(cgm_df['Date time'] >= start_list[j]) & (cgm_df['Date time'] < end_list[j])]
            cgm_df.at[i,'Meal or no meal'] = 0
            if pd.isna(cgm_df.at[i,'Sensor Glucose (mg/dL)']):
                t1 += 1
            list4.append(cgm_df.at[i,'Sensor Glucose (mg/dL)'])
    if t1 == 0 and len(list4) == 24:
        list3.append(list4)

# download the mealdata.csv file #

with open("mealdata.csv","w+", newline='') as my_csv:
    csvWriter = csv.writer(my_csv)
    csvWriter.writerows(list1)

# drop  last six columnns in meal data #

meal_df = pd.read_csv("mealdata.csv") 

for i in range(6):
    meal_df = meal_df.drop(meal_df.columns[-1],axis=1)

meal_df.to_csv('mealdata.csv',index=False)

# download the nomealdata.csv file #

with open("nomealdata.csv","w+", newline='') as my_csv:
    csvWriter = csv.writer(my_csv)
    csvWriter.writerows(list3)


# In[4]:


reader = csv.reader(open("mealdata.csv",newline=''))
reader1 = csv.reader(open("mealdata1.csv",newline=''))
f = open("meald.csv", "w", newline='')
writer = csv.writer(f)

for row in reader:
    writer.writerow(row)
for row in reader1:
    writer.writerow(row)
f.close()


# In[ ]:


reader = csv.reader(open("nomealdata.csv",newline=''))
reader1 = csv.reader(open("nomealdata1.csv",newline=''))
f = open("nomeal.csv", "w", newline='')
writer = csv.writer(f)

for row in reader:
    writer.writerow(row)
for row in reader1:
    writer.writerow(row)
f.close()


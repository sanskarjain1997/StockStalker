import pandas as pd
import numpy as np
from datetime import datetime, timedelta

data = {} #for structured data
SYMBOL = 'INFY'
date = {'2014':['FEB','JUN','MAY'], '2016':['SEP'], '2017':[''], '2018': [''], '2019': ['JAN','FEB']}
columns = ['date','time','open', 'high', 'low', 'close','volumn']

hist = [] #for whole data

for year in date.keys():
	data[year]={}
	for month in date[year]:
		data[year][month] = pd.read_csv(SYMBOL+'/'+SYMBOL+'-'+month+'-'+year+'.csv',index_col=False, names=columns)
		data[year][month] = [x for x in data[year][month].groupby('date')] #making tuples of date and daily data, for grouping
		hist = hist + [data[year][month][i][1] for i in range(0, len(data[year][month]))]
        
ideal_timestamps=[]
opening_time = datetime.strptime('09:16','%H:%M')
for i in range(0,375):
		ideal_timestamps.append(opening_time)
		opening_time+=timedelta(minutes=1)     
itl = [str(k.strftime('%H:%M')) for k in ideal_timestamps]

for h in hist: #setting time as index
	h['time'].astype(str)
	h.set_index('time', inplace=True)

for h in range(0,len(hist)): #removing extra values
	idx = [str(x) for x in hist[h].index]
	rows_to_drop = [str(item) for item in idx if item not in itl]
	print('Rows to drop : ',rows_to_drop)
	hist[h]=hist[h].drop(rows_to_drop)
	
a=[x for x in range(0,len(hist)) if len(hist[x]) != 375] #Identifying index number of days with less than 375 instances
print('\n\n\n\nCorrupted sample indices = ',a)

samples_to_delete=[]

for h in a: #filling missing values
	idx = [str(x) for x in hist[h].index]
	rows_to_add = [str(item) for item in itl if item not in idx]
	print('Rows to Add (index=',h,') : ',rows_to_add)
	if len(rows_to_add) >= 4: 
		print("\tDeleting this sample : too many missing values")
		samples_to_delete.append(h)

	else:
		for row in rows_to_add:
			hist[h].loc[row]=hist[h].iloc[itl.index(row)-1]
			hist[h] = hist[h].sort_index()
			print('\tRow Added!\t current_size=',len(hist[h]))
					
	print('\n')

for i in range(0,len(hist)): 
	if len(hist[i])==0: samples_to_delete.append(i)
	hist[i]=hist[i].reset_index() #Resetting Indices of all samples

for s in samples_to_delete: del hist[s]	#deleting corrupted samples at last

pd.concat(hist).to_csv('Processed-'+SYMBOL+'.csv', sep=',', encoding='utf-8', index=False) #writing processed data into a csv

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pytz
import datetime

ist = pytz.timezone('Asia/Calcutta')
eastern = pytz.timezone('US/Eastern')

API_KEY = 'XR8FXMU9IVDLSPHE'
EXCHANGE = 'NSE:'
SYMBOL  = 'TCS'

ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=EXCHANGE+SYMBOL, interval='1min', outputsize='full')

#for holding IST timestamps
new_dates = []
new_times = []
for date in data.index:
	date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
	date = eastern.localize(date)
	date = date.astimezone(ist)
	date = date.strftime('%d-%b-%Y %H:%M:%S').split(' ')
	new_dates.append(date[0])
	new_times.append(date[1])
	
data = data.set_index([new_dates, new_times])
print(data.iloc[10])
day_grps=[]
for i in range(0,5):
    day_grps.append(data.iloc[375*i:375*(i+1)])


day_grps[-2]['4. close'].plot()
plt.title(EXCHANGE+SYMBOL+' stock (1min)')
plt.show()

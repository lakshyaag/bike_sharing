import calendar as cal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

bike_data = pd.read_csv('data.csv')

# Cleaning up data
bike_data['datetime'] = pd.to_datetime(bike_data['datetime'])

bike_data['date'] = bike_data['datetime'].apply(lambda x: x.date())
bike_data['hour'] = bike_data['datetime'].apply(lambda x: x.hour)
bike_data['weekday'] = bike_data['datetime'].apply(lambda x: cal.day_name[x.weekday()])
bike_data['month'] = bike_data['datetime'].apply(lambda x: cal.month_name[x.month])

bike_data.drop('datetime', axis=1, inplace=True)

bike_data['season'] = bike_data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
bike_data['weather'] = bike_data['weather'].map({
    1: 'Clear, Few clouds, Partly cloudy, Partly cloudy',
    2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
    3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
    4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
})

category_list = ['hour', 'weekday', 'month', 'season', 'weather', 'holiday', 'workingday']

for cat in category_list:
    bike_data[cat] = bike_data[cat].astype('category')


# Handling outliers
bike_data = bike_data[np.abs(bike_data['count'] - bike_data['count'].mean()) <= (3 * bike_data['count'].std())]

# Data Visualization
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(19.20, 10.80))

# Avg. Count by month
months = []
for i in range(1, 13):
    months.append(cal.month_name[i])
month_avg = pd.DataFrame(bike_data.groupby('month')['count'].mean()).reset_index()
f1 = sns.barplot(x='month', y='count', data=month_avg, order=months, ax=axs[0][0])
for i in f1.get_xticklabels():
    i.set_rotation(35)
axs[0][0].set(xlabel='Month', ylabel='Average Count', title='Average Count by Month')

# Avg. User count by hour of day across seasons
hour_avg = pd.DataFrame(bike_data.groupby(['hour', 'season'])['count'].mean()).reset_index()
sns.pointplot(x='hour', y='count', hue='season', data=hour_avg, ax=axs[0][1])
axs[0][1].set(xlabel='Hour', ylabel='Average Count', title='Average Count by Hour of day across Seasons')

# Avg. User count by hour of day across weekdays
weekday_avg = pd.DataFrame(bike_data.groupby(['hour', 'weekday'])['count'].mean()).reset_index()
sns.pointplot(x='hour', y='count', hue='weekday', data=weekday_avg, ax=axs[1][0])
axs[1][0].set(xlabel='Hour', ylabel='Average Count', title='Average Count by Hour of day across Weekdays')

# Avg. User count by hour of day across users

users_avg = pd.melt(bike_data[['hour', 'casual', 'registered']], id_vars=['hour'], value_vars=['casual', 'registered'],
                    var_name='users', value_name='count')
users_avg = pd.DataFrame(users_avg.groupby(['hour', 'users'])['count'].mean()).reset_index()
sns.pointplot(x='hour', y='count', hue='users', data=users_avg, ax=axs[1][1])
axs[1][1].set(xlabel='Hour', ylabel='Average Count', title='Average Count by Hour of day across Users')

plt.savefig('data.png')
